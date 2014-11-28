__author__ = 'brianhoffman'

import constants
from pyee import EventEmitter
import helpers


class PendingPacket():

    def __init__(self, packet, packet_sender):
        print 'Init PendingPacket'

        self.ee = EventEmitter()

        self._packet_sender = packet_sender
        self._packet = packet

    def send(self):
        def packet_send():
            self._packetSender.send(self._packet)

        self._intervalID = helpers.set_interval(
            packet_send,
            constants.TIMEOUT
        )
        self._packet_sender.send(self._packet)

    def get_sequence_number(self):
        return self._packet.get_sequence_number()

    def acknowledge(self):
        self._intervalID.cancel()
        self.ee.emit('acknowledge')
