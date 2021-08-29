from chesscom.crawler import Crawler

archive_date = "2021-07"
crawler = Crawler()

# TODO:
#    seed_players=["hikaru"],
#    seed_tournaments=["titled-tuesday-blitz-june-29-2021-2428655"],
#    output_dir="",
#    filter=None,
#    decorate=None,

crawler \
    .set_date(archive_date) \
    .add_players(["hikaru"]) \
    .crawl()
