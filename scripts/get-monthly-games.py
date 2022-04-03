import sys
import re
from chesscom.crawler import Crawler
from tournaments import tournaments

if len(sys.argv) < 2:
    raise Exception("No date specified. Expected format: YYYY-MM")

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

# archive_date = "2021-08"
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
    .add_tournaments(archivedTournaments) \
    .crawl()

