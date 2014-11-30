from pyee import EventEmitter


class Packet:

    def __init__(self, sequence_number, payload, synchronize, reset=None):
        print 'Init Packet'

        self.ee = EventEmitter()

        self.segment = sequence_number
        self.offset = 0

        self._acknowledgement = False
        self._synchronize = bool(synchronize)
        self._finish = False
        self._reset = bool(reset)
        self._sequenceNumber = sequence_number
        self._payload = payload

    @staticmethod
    def createAcknowledgementPacket(sequenceNumber):
        packet = Packet(sequenceNumber, '', False)
        packet._acknowledgement = True
        return packet

    @staticmethod
    def createFinishPacket():
        packet = Packet(0, '', False, False)
        packet._finish = True
        return packet

    def __eq__(self, other):
        return (
            self._acknowledgement is other._acknowledgement and
            self._synchronize is other._synchronize and
            self._finish is other._finish and
            self._reset is other._reset and
            self._sequenceNumber is other._sequenceNumber and
            self._payload is other._payload
        )

    def get_sequence_number(self):
        return self._sequenceNumber

