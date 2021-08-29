import os
from typing import List
from chesscom.archive import Archive

from config import ARCHIVE_ROOT

PLAYER_GAMES_DIR = os.path.join(ARCHIVE_ROOT, "players")

player = "hikaru"
date = "2021-07"

archive = Archive()
game_data = archive.fetch_player_game_archive(player, date)


def line_starts_with(lines: List[str], text: str) -> int:
    for index, line in enumerate(lines):
        if line.startswith(text):
            return index
    return False

def decorate_pgn(game):
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

    game["pgn"] = "\n".join(lines)
    return game


games_as_pgn = [
    decorate_pgn(game)["pgn"]
    for game in game_data["games"]
    if (
        game["rules"] == "chess"
        and game["time_class"] in ["blitz", "rapid", "daily"]
    )
]

file_name = f"{player}-{date}.pgn"
file_path = f"{PLAYER_GAMES_DIR}/{file_name}"
print(f"[PGN] Saving {len(games_as_pgn)} games to {file_name}")

with open(file_path, 'w') as f:
    for item in games_as_pgn:
        f.write("%s\n" % item)
