import hashlib
from typing import List

def by_score(player) -> int:
    return int(float(player.points) * 2)


def hash_string(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def hash_shard(text: str, length: int = 4) -> str:
    return hash_string(text)[0:length]


def flatten_dict(data: dict, field_names: List[str]):
    data = data.copy()
    for key in field_names:
        if key in data and isinstance(data[key], dict):
            data.update(data[key])
            del data[key]

    return data


def line_starts_with(lines: List[str], text: str) -> int:
    for index, line in enumerate(lines):
        if line.startswith(text):
            return index
    return False

