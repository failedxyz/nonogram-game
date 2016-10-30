from cStringIO import StringIO

from flask import session

from client import Client
from data import clients, channels
from util import decrypt


class Packet:
    def __init__(self, client):
        self.client = client

    def handle(self):
        raise NotImplementedError("%s handler not implemented." % self.__class__.__name__)

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
        data = decrypt(raw_data, client.connection_key)
        if pid == 2:
            return ChannelInfoPacket(client)
        return Packet()


class ConnectionPacket(Packet):
    def handle(self):
        session["uid"] = self.client.uid
        obj = dict(key=self.client.connection_key)
        return 1, obj


class ChannelInfoPacket(Packet):
    def handle(self):
        result = []
        for cname in channels:
            channel = channels[cname]
            result.append({
                "name": cname,
                "autojoin": channel.autojoin
            })
        return 2, result
