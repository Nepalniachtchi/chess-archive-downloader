from chesscom.archive import Archive
from chesscom.utils import by_score


## Titled Tuesday tournaments
# tournament = "titled-tuesday-blitz-june-29-2021-2428655"

## Daily Championship tournaments -- needs scaffold of top-level doc
# tournament = "2021-chess-com-daily-chess-championship"
# tournament = "2020-chess-com-daily-chess-championship"

archive = Archive()
# archive.add_tournament(tournament)

# tournament = archive.get_tournament(tournament)
# players = tournament.players

# for players in sorted(tournament.players, key=by_score, reverse=True):
#     rating_diff = (players.rating_hi or 0) - (players.rating_lo or 0)
#     print(f"{players.points}\t{players.rating_lo}-{players.rating_hi}  {rating_diff}\t{players.username}")



# Titled Tuesday tournaments
tournaments = [
    # August 2021
    "titled-tuesday-blitz-august-24-2021-2533344",
    "titled-tuesday-blitz-august-17-2021-2528831",
    "titled-tuesday-blitz-august-10-2021-2514265",
    "titled-tuesday-blitz-august-03-2021-2500049",

    # July 2021
    "titled-tuesday-blitz-july-27-2021-2485661",
    "titled-tuesday-blitz-july-20-2021-2471236",
    "titled-tuesday-blitz-july-13-2021-2457070",
    "titled-tuesday-blitz-july-06-2021-2443189",

    # June 2021
    "titled-tuesday-blitz-june-29-2021-2428655",
    "titled-tuesday-blitz-june-22-2021-2413621",
    "titled-tuesday-blitz-june-15-2021-2399019",
    "titled-tuesday-blitz-june-08-2021-2384337",
    "titled-tuesday-blitz-june-01-2021-2359358",

    # May 2021
    "titled-tuesday-blitz-may-25-2021-2333682",
    "titled-tuesday-blitz-may-18-2021-2319376",
    "titled-tuesday-blitz-may-11-2021-2314015",
    "titled-tuesday-blitz-may-4-2021-2288851",

]
for tournament in tournaments:
    archive.add_tournament(tournament)
