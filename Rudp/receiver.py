from packet import Packet
from linkedlist import LinkedList
import constants

from pyee import EventEmitter


class Receiver():

    def __init__(self, packet_sender):
        print 'Init Receiver'

        # TODO: have this be a DuplexStream instead of an EventEmitter.
        # TODO: the Receiver should never send raw packets to the end host. It should
        #      only be acknowledgement packets. Please see [1]

        self.ee = EventEmitter()

        self._synced = False
        self._next_sequence_number = 0

        def sort_by_sequence(packet_a, packet_b):
            return packet_a.get_sequence_number() - packet_b.get_sequence_number()

        self._packets = LinkedList(sort_by_sequence)
        self._packet_sender = packet_sender
        self._closed = False


    def receive(self, packet):
        if self._closed:
            # Since this is closed, don't do anything.
            return

        # Ignores packets that have a sequence number less than the next sequence
        # number
        if not packet.getIsSynchronize() and packet.getSequenceNumber() < self._sync_sequence_number:
            return

        if packet.getIsSynchronize() and not self._synced:
            # This is the beginning of the stream.

            if packet.getSequenceNumber() is self._sync_sequence_number:
              self._packet_sender.send(Packet.createAcknowledgementPacket(packet.getSequenceNumber()))
              return

            # Send the packet upstream, send acknowledgement packet to end host, and
            # increment the next expected packet.
            self._packets.clear()
            self.ee.emit('data', packet.getPayload())
            self._packet_sender.send(Packet.createAcknowledgementPacket(packet.getSequenceNumber()))
            self._packets.insert(packet)
            self._next_sequence_number = packet.getSequenceNumber() + 1
            self._synced = True
            self._sync_sequence_number = packet.getSequenceNumber()


            if packet.getIsReset():
                self.ee.emit('_reset')
                self._synced = False

            # We're done.
            return

        elif (packet.getIsReset()):
            self.ee.emit('_reset')
            self.ee._synced = False

        elif not self._synced:
            # If we are not synchronized with sender, then this means that we should
            # wait for the end host to send a synchronization packet.

            # We are done.
            return

        elif packet.getSequenceNumber() < self._syncSequenceNumber:
            # This is a troll packet. Ignore it.
            return

        elif packet.getSequenceNumber() >= (self._packets.currentValue().getSequenceNumber() + constants.WINDOW_SIZE):
            # This means that the next packet received is not within the window size.
            self.ee.emit('_window_size_exceeded')
            return

        # This means that we should simply insert the packet. If the packet's
        # sequence number is the one that we were expecting, then send it upstream,
        # acknowledge the packet, and increment the next expected sequence number.
        #
        # Once acknowledged, check to see if there aren't any more pending packets
        # after the current packet. If there are, then check to see if the next
        # packet is the expected packet number. If it is, then start the
        # acknowledgement process anew.

        result = self._packets.insert(packet)

        if result is LinkedList.InsertionResult.INSERTED:
            self._pushIfExpectedSequence(packet)
        elif result is LinkedList.InsertionResult.EXISTS:
            self._packet_sender.send(Packet.createAcknowledgementPacket(packet.getSequenceNumber()))

    def _pushIfExpectedSequence(self, packet):
        if packet.get_sequence_number() is self._next_sequence_number:
            self.ee.emit('data', packet.getPayload())
            # [1] Never send packets directly!
            self._packet_sender.send(Packet.createAcknowledgementPacket(packet.getSequenceNumber()))
            self._nextSequenceNumber += 1
            self._packets.seek()
            if self._packets.hasNext():
              self._pushIfExpectedSequence(self._packets.nextValue())


    def end(self):
        self._closed = True
        self.ee.emit('end')
