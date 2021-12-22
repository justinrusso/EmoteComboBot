import json
import os


class Store:
    def __init__(self, path: str):
        self.path = f'store/{path}'
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.data = json.loads(f.read())
        else:
            self.data = {'count': 0, 'emote': None}
            self.save()

    def save(self):
        with open(self.path, 'w+') as outfile:
            json.dump(self.data, outfile)
