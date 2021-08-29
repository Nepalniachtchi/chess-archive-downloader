import os
import sys
import json
import logging
from datetime import datetime
from chesscom.archive import Archive
from bloom_filter2 import BloomFilter

from config import CACHE_ROOT

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


def next_cache_file(root_dir: str):
    for root, _, files in os.walk(root_dir):
        cache_dir = os.path.basename(root)
        for filename in files:
            if filename.endswith(".json"):
                yield f"{cache_dir}/{filename}"


class DailyGameProcessor():
    def __init__(self):
        self.archive_dir = f"{CACHE_ROOT}/games"
        self.daily_dir = f"{CACHE_ROOT}/daily"
        self.archive = Archive()
        self.date = None
        self.seen_players=BloomFilter(max_elements=100000, error_rate=0.001)
    
    def set_date(self, date: str):
        self.date = date
        return self

    def mark_player_as_seen(self, player: str):
        self.seen_players.add(player)

    def has_seen_player(self, player) -> bool:
        return player in self.seen_players

    def game_filter(self, game) -> bool:
        return (
            game["rules"] == "chess"
            and game["time_class"] in ["rapid", "blitz", "daily"]
            and game["white"]["rating"] >= 1950
            and game["black"]["rating"] >= 1950
            and not self.has_seen_player(game["white"]["username"])
            and not self.has_seen_player(game["black"]["username"])
        )

    def filter_games(self, games, game_filter):
        return [
            game
            for game in games
            if (game_filter(game))
        ]

    def prep_game(self, game):
        _, game_id = game["url"].rsplit("/", 1)
        game_time = datetime.utcfromtimestamp(game["end_time"]).strftime("%Y-%m-%dT%H:%M:%SZ")

        cleaned_game = {
            "date": game_time,
            "id": game_id,
        }

        cleaned_game.update(game)
        return cleaned_game

    def split_games_into_days(self, games):
        daily_games = {}
        error_count = 0
        for game in games:
            if "pgn" not in game:
                error_count += 1
                continue

            end_date = datetime.utcfromtimestamp(game["end_time"]).strftime('%Y-%m-%d')
            if end_date not in daily_games:
                daily_games[end_date] = []
            
            daily_games[end_date].append(self.prep_game(game))

        return daily_games, error_count

    def load_games(self, archive_file):
        with open(f"{archive_file}", 'r', encoding='utf-8') as archive_file:
            game_archive = json.load(archive_file)
            return game_archive["_data"]["games"]

    def append_daily_games(self, daily_games):
        for day in daily_games.keys():
            with open(f"{self.daily_dir}/{self.date}/{day}.jsons", "a") as outfile:
                for game in daily_games[day]:
                    json.dump(game, outfile)
                    outfile.write("\n")

    def start(self):
        logger.debug(f"[START] GameProcessor ({self.date})")
        total = 0

        os.makedirs(os.path.join(self.daily_dir, self.date), exist_ok=True)
        cache_dir = f"{self.archive_dir}/{self.date}"

        for cache_file in next_cache_file(cache_dir):
            username = os.path.splitext(os.path.basename(cache_file))[0]
            archived_games = self.load_games(f"{cache_dir}/{cache_file}")
            games = self.filter_games(archived_games, self.game_filter)
            logger.info(f"[{total:0>5}] {cache_file}: Games {len(archived_games)} => {len(games)} games")
            daily_games, error_count = self.split_games_into_days(games)
            self.append_daily_games(daily_games)

            if error_count == 0:
                self.mark_player_as_seen(username)
            else:
                logger.info(f"[WARN] {username} Skipped {error_count} games with no PGN")

            total += 1

        logger.debug(f"[END] GameProcessor ({self.date})")
