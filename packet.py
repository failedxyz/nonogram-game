from cStringIO import StringIO

from flask import session

from client import Client
from data import clients


class Packet:
    @classmethod
    def parse(cls, data):
        stream = StringIO(data)
        pid = int(stream.read(3))
        if pid == 1:
            client = Client()
            clients[client.uid] = client
            return ConnectionPacket(client)


class ConnectionPacket(Packet):
    def __init__(self, client):
        self.client = client

    def handle(self):
        session["uid"] = self.client.uid
        print "SESSION", session
        obj = dict(key=self.client.connection_key)
        return 1, obj
