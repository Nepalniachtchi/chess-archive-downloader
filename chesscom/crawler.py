import sys
import logging
from typing import List
from bloom_filter2 import BloomFilter

from chesscom.archive import Archive

logger = logging.getLogger("")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

class Crawler():
    def __init__(self) -> None:
        self.archive = Archive()
        self.date = None
        self.queue = []

        self.count = 0
        self.seen_players=BloomFilter(max_elements=3000000, error_rate=0.001)

    def filter_seen_players(self, players: List[str]) -> List[str]:
        return [player for player in players if player not in self.seen_players]

    def mark_player_as_seen(self, player: str):
        self.seen_players.add(player)

    def set_date(self, date: str):
        self.date = date
        return self

    def add_players(self, players: List[str]):
        players = self.filter_seen_players(players)
        self.queue = list(set(self.queue + players))
        return self

    def add_tournament(self, tournament_id: str):
        self.archive.add_tournament(tournament_id)
        tournament = self.archive.get_tournament(tournament_id)
        players = [
            player.username
            for player in tournament.players
            if (
                player.rating_hi and player.rating_hi >= 1950
                and player.username not in self.queue
            )
        ]
        logger.info(f"[PLAYERS] Adding {len(players)} players from {tournament_id}")
        self.add_players(players)
        return self

    def add_tournaments(self, tournaments: List[str]):
        [self.add_tournament(tournament) for tournament in tournaments]
        return self

    def get_next_player(self) -> str:
        return self.queue.pop(0)

    def get_players_from_games(self, games: List[dict]) -> List[str]:
        player_lookup = {}

        for game in games:
            for player in [game["white"], game["black"]]:
                username = player["username"].lower()

                if username in player_lookup:
                    player_lookup[username]["min_rating"] = min([
                        player["rating"],
                        player_lookup[username]["min_rating"]
                    ])
                    player_lookup[username]["max_rating"] = max([
                        player["rating"],
                        player_lookup[username]["min_rating"]
                    ])
                else:
                    player_lookup[username] = {
                        "username": username,
                        "max_rating": player["rating"],
                        "min_rating": player["rating"]
                    }

        return player_lookup.values()


    def crawl_player(self, player: str):
        game_data = self.archive.fetch_player_game_archive(player, self.date)

        if game_data is not None:
            opponents = self.get_players_from_games(game_data["games"])

            self.add_players([
                opponent["username"]
                for opponent in opponents
                if opponent["username"] != player
                and opponent["max_rating"] >= 1950
            ])
        else:
            logger.info(f"[PLAYER] {player} not found")


    def crawl(self):
        logger.info(f"[START] Crawler ({self.date})")

        try:
            while True:
                player = self.get_next_player()
                self.mark_player_as_seen(player)
                logger.info(f"[{self.count}/{self.count + len(self.queue)}] Player: {player}")
                self.crawl_player(player)
                self.count += 1

        except IndexError:
            logger.info(f"[END] Crawler ({self.date})")
