import sys
from chesscom.processor import DailyGameProcessor

# Turns the monthly player archives into per-day files
# 
# Reads monthly archive in ./_cache/games/YYYY-MM
# Writes daily files to ./_cache/daily/YYYY-MM

archive_date = sys.argv[1]

processor = DailyGameProcessor()

processor \
    .set_date(archive_date) \
    .start()
