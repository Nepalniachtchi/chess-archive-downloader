import os
import time
import logging
import chessdotcom
from chessdotcom.client import ChessDotComError

from config import CACHE_ROOT

from .cache import JsonFileCache as Cache
from .utils import hash_shard

logger = logging.getLogger(__name__)

class ChessComClient():
    def __init__(self):
        self.tournament_cache = Cache(os.path.join(CACHE_ROOT, "tournaments"))
        self.game_cache = Cache(os.path.join(CACHE_ROOT, "games"))

    def get_tournament(self, tournament_id: str):
        tournament_shard = hash_shard(tournament_id)
        cache_key = f"{tournament_shard}/{tournament_id}"
        if self.tournament_cache.has(cache_key):
            logger.debug(f"[CHESSCOM] Cache hit {cache_key}")
            return self.tournament_cache.get(cache_key)
        else:
            response = chessdotcom.get_tournament_details(tournament_id)
            tournament = response.json["tournament"]
            self.tournament_cache.set(cache_key, tournament)
            return tournament

    def get_tournament_round(self, tournament_id: str, round: str):
        tournament_shard = hash_shard(tournament_id)
        cache_key = f"{tournament_shard}/{tournament_id}.{round}"
        if self.tournament_cache.has(cache_key):
            logger.debug(f"[CHESSCOM] Cache hit {cache_key}")
            return self.tournament_cache.get(cache_key)
        else:
            response = chessdotcom.get_tournament_round(tournament_id, round)
            round = response.json["tournament_round"]
            self.tournament_cache.set(cache_key, round)
            return round

    def get_tournament_round_group(self, tournament_id:str, round: str, group: str):
        tournament_shard = hash_shard(tournament_id)
        cache_key = f"{tournament_shard}/{tournament_id}.{round}.{group}"
        if self.tournament_cache.has(cache_key):
            logger.debug(f"[CHESSCOM] Cache hit {cache_key}")
            return self.tournament_cache.get(cache_key)
        else:
            response = chessdotcom.get_tournament_round_group_details(tournament_id, round, group)
            group = response.json["tournament_round_group"]
            self.tournament_cache.set(cache_key, group)
            return group

    def get_player_games_by_month(self, username: str, date: str, retry_wait: int=5):
        # cache_key = f"player.{username}.{date}"
        user_shard = hash_shard(username)
        cache_key = f"{date}/{user_shard}/{username}"
        games_archive = None

        if self.game_cache.has(cache_key):
            logger.debug(f"[CHESSCOM] Cache hit {cache_key}")
            return self.game_cache.get(cache_key)
        else:
            year, month = date.split('-')
            logger.info(f"[ARCHIVE] {username} {year}-{month}")

            try:
                response = chessdotcom.get_player_games_by_month(username, year=year, month=month)
                games_archive = response.json
                self.game_cache.set(cache_key, games_archive)
            except ChessDotComError as e:
                logger.warning(f"[ERROR] for {username} {date}: {e}")
            except TypeError as e:
                logger.warning(f"[ERROR] TypeError for {username} {date}: {e}")
            except ConnectionResetError as e:
                logger.warning(f"[ERROR] Connection reset for {username} {date}: {e}")

        return games_archive
