from data import channels


class Channel:
    def __init__(self, name, autojoin=False, add=True):
        self.name = name
        self.autojoin = autojoin
        self.type = "chat"
        if add:
            channels[name] = self
