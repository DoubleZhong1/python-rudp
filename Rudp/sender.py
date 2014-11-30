from packet import Packet
from pendingpacket import PendingPacket
import constants
import helpers
import math
import random

from pyee import EventEmitter


class Window():

    def __init__(self, packets):
        print 'Init Window'

        self.ee = EventEmitter()

        self._packets = packets

    def send(self):
        # Our packets to send.
        pkts = self._packets

        # The initial synchronization packet. Always send this first.
        self._synchronization_packet = pkts.pop(0)

        # The final reset packet. It can be equal to the synchronization packet.
        self._reset_packet = pkts.pop() if len(pkts) else self._synchronization_packet

        # This means that the reset packet's acknowledge event thrown will be
        # different from that of the synchronization packet.
        if self._reset_packet is not self._synchronization_packet:
            @self._reset_packet.ee.on('acknowledge')
            def on_acknowledge():
                self.ee.emit('done')

        # Will be used to handle the case when all non sync or reset packets have
        # been acknowledged.
        @self._synchronization_packet.ee.on('acknowledge')
        def on_sync_knowledge():
            # We will either notify the owning class that this window has finished
            # sending all of its packets (that is, if this window only had one packet
            # in it), or keep looping through each each non sync-reset packets until
            # they have been acknowledged.
            if self._reset_packet is self._synchronization_packet:
                self.ee.emit('done')
                return
            elif len(pkts) is 0:
                # This means that this window only had two packets, and the second one
                # was a reset packet.
                self._reset_packet.send()
                return

            @self.ee.on('acknowledge')
            def on_sender_acknowledge():
                # This means that it is now time to send the reset packet.
                self._reset_packet.send()

            # And if there are more than two packets in this window, then send all
            # other packets.
            self.acknowledged = 0

            for packet in pkts:
                @packet.ee.on('acknowledge')
                def on_packet_acknowledge():
                    self.acknowledged += 1
                    if self.acknowledged is len(pkts):
                        self.ee.emit('acknowledge')

                packet.send()

        self._synchronization_packet.send()

    def verify_acknowledgement(self, sequence_number):
        for i in range(0, len(self._packets)):
            if self._packets[i].get_sequence_number() is sequence_number:
                self._packets[i].acknowledge()


class Sender:

    def __init__(self, packet_sender):
        print 'Init Sender'

        self._packet_sender = packet_sender
        self._windows = []
        self._sending = None

    def send(self, data):
        chunks = helpers.splitArrayLike(data, constants.UDP_SAFE_SEGMENT_SIZE)
        windows = helpers.splitArrayLike(chunks, constants.WINDOW_SIZE)
        self._windows = self._windows + windows
        self._push()

    def _push(self):
        if not self._sending and len(self._windows):
            self._base_sequence_number = math.floor(random.random() * (constants.MAX_SIZE - constants.WINDOW_SIZE))
            window = self._windows.pop(0)

            def get_packet(i, pdata):
                packet = Packet(float(i) + self._base_sequence_number, pdata, not i, i is (len(window) - 1))
                return PendingPacket(packet, self._packet_sender)

            win = [get_packet(i, data) for i, data in enumerate(window)]
            to_send = Window(win)

            self._sending = to_send

            @self._sending.ee.on('done')
            def on_done():
                self._sending = None
                self._push()

            to_send.send()

    def verifyAcknowledgement(self, sequence_number):
        if self._sending:
            self._sending.verifyAcknowledgement(sequence_number)
