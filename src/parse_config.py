import pathlib
import json


class Config:
    def __init__(self, path):
        self.path = path

        self.data = {}
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Error: configuration file not found:\n{self.path}")
        except json.JSONDecodeError as e:
            print(f"Decode error:\n{e}")
        except PermissionError:
            print(f"Error: cant access configuration file, permision denied\n{self.path}")

    def rules(self) -> dict:
        return self.data.get("rules", {})

    def ignore(self) -> set:
        converted = set(map(lambda x: pathlib.Path(x).absolute(), self.data.get("ignore", {})))
        return converted 

class TestConfig(Config):
    def __init__(self, rules={}, ignore={}):
        self.data = {}
        self.data["rules"] = rules
        self.data["ignore"] = ignore

if __name__ == "__main__":
    config = Config("../config.json")
    config2 = TestConfig()

    print(config.rules())
    print(config.ignore())
