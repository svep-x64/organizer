import json

class Config:
    def __init__(self, path):
        self.path = path

    def parse(self) -> dict:
        with open(self.path, "r") as file:
            data = json.load(file)
        data.pop('ignore', None)
        return data

    def ignore(self) -> list:
        with open(self.path, "r") as file:
            data = json.load(file)
        return data.get('ignore', None)

