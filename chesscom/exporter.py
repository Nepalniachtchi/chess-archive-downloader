from chesscom.utils import line_starts_with
import os
import sys
import json
import logging

from config import CACHE_ROOT, PGN_ROOT

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class GameExporter():
    def __init__(self):
        self.daily_dir = f"{CACHE_ROOT}/daily"
        self.pgn_dir = f"{PGN_ROOT}/daily"
        self.date = None

    def set_date(self, date):
        self.date = date
        return self

    def get_daily_files(self):
        files = [
            file
            for file in os.listdir(f"{self.daily_dir}/{self.date}")
            if file.endswith('.jsons')
        ]
        files.sort()
        return files
    
    def extract_pgn(self, game):
        if "pgn" not in game:
            # print(game)
            logger.warn(f"[GAME] No PGN {game['id']} {game['white']['username']} - {game['black']['username']}")
            return False

        lines = game["pgn"].split("\n")

        # Update Event header
        event_index = line_starts_with(lines, "[Event ")
        if event_index is not False:
            event_line = lines[event_index]
            event_line = (
                event_line[0:-2]
                + f" - {'Rated' if game['rated'] else 'Unrated'} {game['time_class'].capitalize()}"
                + event_line[-2:]
            )
            lines[event_index] = event_line

        # Add in new headers
        separator_index = lines.index("")
        lines[separator_index:separator_index] = [
            f'[ChesscomId "{game["id"]}"]'
        ]

        game_pgn = "\n".join(lines)
        return game_pgn

    def export_games(self, from_file, pgn_file):
        game_count = 0
        error_count = 0
        with open(f"{self.daily_dir}/{self.date}/{from_file}", "r") as input_file:
            with open(f"{self.pgn_dir}/{self.date}/{pgn_file}", "w") as output_file:
                for index, json_doc in enumerate(input_file):
                    game = json.loads(json_doc)
                    # logger.debug(f"[GAME] {game}")
                    pgn_game = self.extract_pgn(game)

                    if pgn_game is not False:
                        # logger.debug(f"[GAME] PGN: {pgn_game}")
                        output_file.write(pgn_game + "\n")
                        game_count = index
                        # break
                    else:
                        error_count += 1

        logger.info(f"[EXPORT] Exported {game_count + 1} games to {pgn_file} ({error_count} Skipped)")
        return game_count + 1
                    
    def start(self):
        logger.info(f"[START] Export {self.date}")

        os.makedirs(f"{self.pgn_dir}/{self.date}", exist_ok=True)

        daily_files = self.get_daily_files()
        for daily_file in daily_files:
            pgn_file = os.path.basename(daily_file).split(".")[0] + ".pgn"
            logger.info(f"[EXPORT] {daily_file} -> {pgn_file}")
            self.export_games(daily_file, pgn_file)
            # break

        logger.info(f"[END] Export {self.date}")
