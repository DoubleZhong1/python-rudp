from packet import Packet
from sender import Sender
from receiver import Receiver

from pyee import EventEmitter


class Connection:

    def __init__(self, packet_sender):
        print 'Init Connection'

        self.ee = EventEmitter()

        self._sender = Sender(packet_sender)
        self._receiver = Receiver(packet_sender)

        @self._receiver.ee.on('data')
        def on_data(data):
            self.ee.emit('data', data)

    def send(self, data):
        self._sender.send(data)

    def receive(self, packet):
        if packet.getIsAcknowledgement():
            self._sender.verifyAcknowledgement(packet.getSequenceNumber())
        else:
            self._receiver.receive(packet)
