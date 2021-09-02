import sys
from chesscom.exporter import GameExporter

# archive_date = "2021-07"
archive_date = sys.argv[1]

processor = GameExporter()

processor \
    .set_date(archive_date) \
    .start()
