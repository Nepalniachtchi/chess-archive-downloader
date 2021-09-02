import sys
from chesscom.processor import DailyGameProcessor

# archive_date = "2021-07"
archive_date = sys.argv[1]

processor = DailyGameProcessor()

processor \
    .set_date(archive_date) \
    .start()
