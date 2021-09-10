import sys
from chesscom.crawler import Crawler

# archive_date = "2021-07"
archive_date = sys.argv[1]

crawler = Crawler()
crawler \
    .set_date(archive_date) \
    .add_players(["hikaru"]) \
    .add_tournaments([
        "2021-chess-com-daily-chess-championship",
    ]) \
    .crawl()
