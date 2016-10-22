import json
from cStringIO import StringIO

from flask import session
from flask_socketio import emit

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
        print "SESSION", session
        session["SHIET"] = "SHIET"
        obj = dict(key=self.client.connection_key)
        emit("data", "001%s" % json.dumps(obj))
