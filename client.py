import util
from data import clients


class Client:
    def __init__(self):
        self.uid = util.generate_string()
        while self.uid in clients:
            self.uid = util.generate_string()
        self.connection_key = util.generate_string()
