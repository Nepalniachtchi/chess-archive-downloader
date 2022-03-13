import sys
import re
from chesscom.crawler import Crawler
from .tournaments import tournaments

if len(sys.argv) < 2:
    raise Exception("No date specified. Expected format: YYYY-MM")

<<<<<<< HEAD
=======
# Call with:
#  python -m scripts.get-monthly-games 2021-11
# 
# Parameter is the month in YYYY-MM format.
#
# The main crawler
# * add_players([]...]) -- list of players to seed
# * add_tournaments([...]) -- list of tournaments to seed
#
# Caches player archives in ./_cache/games/YYYY-MM/

# archive_date = "2021-07"
>>>>>>> 6156a83ddde9787904e785ee3d0d502cf8310793
archive_date = sys.argv[1]

if not re.match("^\d{4}\-\d{2}$", archive_date):
    raise Exception("Invalid date specified. Expected format: YYYY-MM")

year = archive_date[:4]
archivedTournaments = tournaments[year] + tournaments[archive_date]
print('Tournaments:', archivedTournaments)

crawler = Crawler()
crawler \
    .set_date(archive_date) \
    .add_players(["hikaru"]) \
<<<<<<< HEAD
    .add_tournaments(archivedTournaments) \
=======
    .add_tournaments([
        # November 2021 Titled Tuesday
        "titled-tuesday-blitz-november-30-2021-2764222",
        "titled-tuesday-blitz-november-23-2021-2750236",
        "titled-tuesday-blitz-november-16-2021-2736618",
        "titled-tuesday-blitz-november-09-2021-2710127",
        "titled-tuesday-blitz-november-02-2021-2688099",
    ]) \
>>>>>>> 6156a83ddde9787904e785ee3d0d502cf8310793
    .crawl()

