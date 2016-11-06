from client import Client
from data import channels


class Channel:
    def __init__(self, name, autojoin=False, add=True):
        self.clients = {}
        self.name = name
        self.autojoin = autojoin
        self.type = "chat"
        if add:
            channels[name] = self

    def __contains__(self, item):
        if isinstance(item, Client):
            return item.uid in self.clients
        return False

    def add_client(self, client):
        self.clients[client.uid] = client

    def json(self):
        return {
            "name": self.name,
            "autojoin": self.autojoin,
            "type": self.type
        }
