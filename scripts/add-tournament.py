import sys
import re
from chesscom.archive import Archive
from chesscom.utils import by_score
from tournaments import tournaments

if len(sys.argv) < 2:
    raise Exception("No date specified. Expected format: YYYY-MM")

archive_date = sys.argv[1]

if not re.match("^\d{4}\-\d{2}$", archive_date):
    raise Exception("Invalid date specified. Expected format: YYYY-MM")

year = archive_date[:4]
archivedTournaments = tournaments[year] + tournaments[archive_date]
print('Tournaments:', archivedTournaments)

archive = Archive()
for tournament in archivedTournaments:
    archive.add_tournament(tournament)


exit()

