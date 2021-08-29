from chesscom.exporter import GameExporter

archive_date = "2021-07"

processor = GameExporter()

processor \
    .set_date(archive_date) \
    .start()
