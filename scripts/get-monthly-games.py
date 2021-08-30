from chesscom.crawler import Crawler

archive_date = "2021-07"
crawler = Crawler()

crawler \
    .set_date(archive_date) \
    .add_players(["hikaru"]) \
    .crawl()

# # Example of seeing players from tournamnents
# crawler \
#     .set_date(archive_date) \
#     .add_players(["hikaru"]) \
#     .add_tournaments([
#         "titled-tuesday-blitz-july-27-2021-2485661",
#         "titled-tuesday-blitz-july-20-2021-2471236",
#         "titled-tuesday-blitz-july-13-2021-2457070",
#         "titled-tuesday-blitz-july-06-2021-2443189",
#     ]) \
#     .crawl()
