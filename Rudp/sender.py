from Rudp.packet import Packet


class Connection:

    def __init__(self, packet_sender):
        print 'Init Connection'

        self._sender = Sender(packet_sender);
        self._receiver = Receiver(packet_sender);

        this._receiver.on('data', function (data) {
            self.emit('data', data)
        });


    def send(self, packet):
        buffer = packet.toBuffer()
        self._socket.send(buffer, 0, buffer.length, self._port, self._address)
