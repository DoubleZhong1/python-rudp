__author__ = 'brianhoffman'

import socket
import sys

from Rudp.client import Client


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client = Client(sock, 'localhost', 12345)

while 1:
    try:
        data = sys.stdin.readline()
    except KeyboardInterrupt:
        break

    if not data:
        break

    client.send(data)
    print data.strip()

