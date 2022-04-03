import logging

from chesscom.client import ChessComClient
from chesscom.utils import flatten_dict, hash_shard
from chesscom.tournaments import init_tournaments, Tournament

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Archive():
    def __init__(self):
        self.client = ChessComClient()
        self.tournaments = init_tournaments()

    def fetch_tournament(self, tournament_id: str) -> Tournament:
        tournament_data = self.client.get_tournament(tournament_id)
        tournament_data["id"] = tournament_id
        url_path = tournament_id + "/"

        player_map = dict()

        for round_url in tournament_data["rounds"]:
            round_no = round_url.split(url_path, 1)[1]
            logger.info(f"[TOURNAMENT] Adding: R.{round_no}")
            round_data = self.client.get_tournament_round(tournament_id, round_no)
            round_url = url_path + round_no + "/"

            for player in round_data["players"]:
                username = player["username"].lower()
                if username not in player_map:
                    player_map[username] = player

            for group_url in round_data["groups"]:
                group_no = group_url.split(round_url, 1)[1]
                logger.info(f"[TOURNAMENT] Adding: R.{round_no} G.{group_no}")
                group_data = self.client.get_tournament_round_group(tournament_id, round_no, group_no)

                for player in group_data["players"]:
                    username = player["username"]
                    player_map[username]["points"] = player["points"]

                # Update rating range for players
                for games in group_data["games"]:
                    for side in ["white", "black"]:
                        game_player = games[side]
                        if not isinstance(game_player, dict):
                            continue
                        username = game_player["username"].lower()
                        rating = game_player["rating"]

                        player = player_map[username]
                        if "rating_lo" not in player or player["rating_lo"] > rating:
                            player["rating_lo"] = rating

                        if "rating_hi" not in player or player["rating_hi"] < rating:
                            player["rating_hi"] = rating

        tournament_data = flatten_dict(tournament_data, ["settings"])
        tournament_data["players"] = list(player_map.values())
        tournament = Tournament(**tournament_data)

        return tournament


    def add_tournament(self, tournament_id: str) -> Tournament:
        if self.tournaments.has_tournament(tournament_id) is False:
            print(f"[TOURNAMENT] Adding: ({hash_shard(tournament_id)}) {tournament_id}")
            tournament = self.fetch_tournament(tournament_id)

            self.tournaments.save_tournament(tournament)
            logger.info(f"[TOURNAMENT] Save: {tournament.id}")

        else:
            logger.info(f"[TOURNAMENT] Already have: {tournament_id}")
            tournament = self.tournaments.load_tournament(tournament_id)

        # for players in sorted(tournament.players, key=by_score, reverse=True):
        #     rating_diff = (players.rating_hi or 0) - (players.rating_lo or 0)
        #     print(f"{players.points}\t{players.rating_lo}-{players.rating_hi}  {rating_diff}\t{players.username}")


    def get_tournament(self, tournament_id: str) -> Tournament:
        return self.tournaments.load_tournament(tournament_id)


    def fetch_player_game_archive(self, username, date: str):
        game_data = self.client.get_player_games_by_month(username, date=date)

        if game_data is not None:
            for game in game_data["games"]:
                game = self._game_as_pgn(game)
                # print("[GAME]", game)

        return game_data

    def _game_as_pgn(self, game):
        _, game_id = game["url"].rsplit("/", 1)
        game["id"] = game_id
        return game
