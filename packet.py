import json
from cStringIO import StringIO

from flask import session

from client import Client
from data import clients, channels
from util import decrypt


class Packet:
    def __init__(self, client, **kwargs):
        self.client = client
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

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
        elif pid == 3:
            return ChannelJoinPacket(client, data=data)
        return Packet(client)


class ConnectionPacket(Packet):
    def handle(self):
        session["uid"] = self.client.uid
        obj = dict(key=self.client.connection_key)
        return 1, obj


class ChannelInfoPacket(Packet):
    def handle(self):
        result = []
        for cname in channels:
            result.append(channels[cname].json())
        return 2, result


class ChannelJoinPacket(Packet):
    def handle(self):
        if not self.data: return
        to_join = json.loads(self.data)
        for channel in to_join:
            if channel in channels and self.client not in channels[channel]:
                channels[channel].add_client(self.client)
        return 3, map(lambda c: c.json(), self.client.channels)
