from chesscom.archive import Archive
from chesscom.utils import by_score

## For pre-loading the tournament JSON documents.
## Archives tournaments to ./_cache/tournaments/

## Daily Championship tournaments -- 
# Note: chess.com public API endpoint fails on these tournaments
# So needs scaffold of top-level doc
# tournament = "2021-chess-com-daily-chess-championship"
# tournament = "2020-chess-com-daily-chess-championship"

archive = Archive()
# archive.add_tournament(tournament)

# Titled Tuesday tournaments
tournaments = [
    # November 2021 - Titled Tuesday tournaments
    "titled-tuesday-blitz-november-30-2021-2764222",
    "titled-tuesday-blitz-november-23-2021-2750236",
    "titled-tuesday-blitz-november-16-2021-2736618",
    "titled-tuesday-blitz-november-09-2021-2710127",
    "titled-tuesday-blitz-november-02-2021-2688099",
]
for tournament in tournaments:
    archive.add_tournament(tournament)
