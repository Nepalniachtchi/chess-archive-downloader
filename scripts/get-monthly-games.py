import sys
from chesscom.crawler import Crawler

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
archive_date = sys.argv[1]

crawler = Crawler()
crawler \
    .set_date(archive_date) \
    .add_players(["hikaru"]) \
    .add_tournaments([
        # November 2021 Titled Tuesday
        "titled-tuesday-blitz-november-30-2021-2764222",
        "titled-tuesday-blitz-november-23-2021-2750236",
        "titled-tuesday-blitz-november-16-2021-2736618",
        "titled-tuesday-blitz-november-09-2021-2710127",
        "titled-tuesday-blitz-november-02-2021-2688099",
    ]) \
    .crawl()
