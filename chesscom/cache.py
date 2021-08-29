import os
import json

CACHE_ROOT = "/tmp/chesscom-cache"

class JsonFileCache():
    def __init__(self, root_dir=CACHE_ROOT):
        self.root = root_dir
        os.makedirs(CACHE_ROOT, exist_ok=True)

    def _get_filepath(self, key: str):
        return os.path.join(self.root, f"{key}.json")

    def has(self, key: str) -> bool:
        return os.path.isfile(self._get_filepath(key))

    def get(self, key: str) -> dict:
        with open(self._get_filepath(key)) as json_file:
            payload = json.load(json_file)
            return payload["_data"]

    def set(self, key: str, data: dict) -> bool:
        filepath = self._get_filepath(key) 
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        payload = {
            "_meta": {},
            "_data": data
        }

        with open(filepath, 'w') as outfile:
            json.dump(payload, outfile)
            return True
