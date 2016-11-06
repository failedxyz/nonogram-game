import util
from data import clients, channels


class Client:
    def __init__(self, add=False):
        self.uid = util.generate_string()
        while self.uid in clients:
            self.uid = util.generate_string()
        self.connection_key = util.generate_string()

    @staticmethod
    def get_by_id(uid):
        if uid in clients.keys():
            return clients[uid]
        return None

    @property
    def channels(self):
        return [channel for channel in channels if self in Channel.get_by_name(channel)]

    def json(self):
        return {
            "uid": self.uid,
            "username": self.username if hasattr(self, "username") else "Guest"
        }


class Channel:
    def __init__(self, name, autojoin=False, add=True):
        self.clients = []
        self.name = name
        self.autojoin = autojoin
        self.type = "chat"
        if add:
            channels[name] = self

    @staticmethod
    def get_by_name(name):
        if name in channels:
            return channels[name]
        return None

    def get_clients(self):
        """ Safe get """
        new_clients = []
        for client in self.clients:
            if Client.get_by_id(client):
                new_clients.append(client)
        self.clients = new_clients
        return new_clients

    def __contains__(self, item):
        if isinstance(item, Client):
            return item.uid in self.get_clients()
        return False

    def add_client(self, client):
        if client in clients and client not in self.clients:
            self.clients.append(client)

    def json(self):
        return {
            "name": self.name,
            "autojoin": self.autojoin,
            "type": self.type,
            "users": [Client.get_by_id(client).json() for client in self.get_clients()]
        }
