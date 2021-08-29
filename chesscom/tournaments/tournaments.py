import json
import os.path

from config import ARCHIVE_ROOT
from .tournament import Tournament

TOURNAMENT_DIR = os.path.join(ARCHIVE_ROOT, "tournaments")

class Tournaments():
    def __init__(self):
        os.makedirs(TOURNAMENT_DIR, exist_ok=True)

    def _get_filepath(self, tournament_id: str) -> str:
        return os.path.join(TOURNAMENT_DIR, f"{tournament_id}.json")

    def has_tournament(self, tournament_id: str) -> bool:
        return os.path.isfile(self._get_filepath(tournament_id))

    def load_tournament(self, tournament_id: str) -> Tournament:
        with open(self._get_filepath(tournament_id)) as json_file:
            payload = json.load(json_file)
            return Tournament(**payload)

    def save_tournament(self, tournament: Tournament) -> bool:
        with open(self._get_filepath(tournament.id), 'w') as outfile:
            outfile.write(tournament.json())
            return True
