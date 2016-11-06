import util
from data import clients, channels


class Client:
    def __init__(self, add=False):
        self.uid = util.generate_string()
        while self.uid in clients:
            self.uid = util.generate_string()
        self.connection_key = util.generate_string()

    @property
    def channels(self):
        return [channel for channel in channels.values() if self in channel]
