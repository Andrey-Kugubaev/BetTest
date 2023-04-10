import json


class Message(object):
    def __init__(self, raw):
        self.raw = raw


class JsonMessage(Message):
    def __init__(self, raw):
        super().__init__(raw)

    def to_dict(self):
        return self.raw

    def to_string(self):
        return json.dumps(self.to_dict())
