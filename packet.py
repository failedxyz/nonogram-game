from cStringIO import StringIO

from flask import session

from client import Client
from data import clients
from util import decrypt


class Packet:
    def handle(self):
        "Do nothing."
        pass

    @classmethod
    def parse(cls, data):
        stream = StringIO(data)
        pid = int(stream.read(3))
        if pid == 1:
            client = Client()
            clients[client.uid] = client
            return ConnectionPacket(client)
        client = clients[session["uid"]]
        raw_data = stream.read()
        print "CLIENT", client.connection_key, raw_data
        data = decrypt(raw_data, client.connection_key)
        print "DATA", data
        if pid == 2:
            print data
        return Packet()


class ConnectionPacket(Packet):
    def __init__(self, client):
        self.client = client

    def handle(self):
        session["uid"] = self.client.uid
        print "SESSION", session
        obj = dict(key=self.client.connection_key)
        return 1, obj
