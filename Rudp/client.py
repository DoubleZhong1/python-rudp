import packet
from packetsender import PacketSender
from connection import Connection

from pyee import EventEmitter


class Client:

    def __init__(self, socket, address, port):
        print 'Init Client'

        ee = EventEmitter()

        self._packet_sender = PacketSender(socket, address, port)
        self._connection = Connection(self._packet_sender)

        @self._connection.ee.on('data')
        def on_data(data):
            ee.emit('data', data)

        def on_message(message, rinfo):
            if rinfo.address is not address or rinfo.port is not port:
                return

            packet = Packet(message)
            if packet.getIsFinish():
                socket.close()
                return

            self._connection.receive(packet)

        #socket.on('message', on_message)


    def send(self, data):
        self._connection.send(data)

    def close(self):
        self._packet_sender.send(Packet.createFinishPacket())

