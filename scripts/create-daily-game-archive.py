from chesscom.processor import DailyGameProcessor

archive_date = "2021-07"

processor = DailyGameProcessor()

processor \
    .set_date(archive_date) \
    .start()
