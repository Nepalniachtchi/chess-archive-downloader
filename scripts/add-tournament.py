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


# Titled Tuesday tournaments
tournaments = [
    # December 2020
    "-titled-tuesday-blitz-1943787",
    "-titled-tuesday-blitz-1913645",
    "-titled-tuesday-blitz-1913631",
    "-titled-tuesday-blitz-1823015",

    # November 2020
    "-titled-tuesday-blitz-1788075",
    "-titled-tuesday-blitz-1722513",
    "-titled-tuesday-blitz-1692727",
    "-titled-tuesday-blitz-1692726",

    #October 2020
    "-titled-tuesday-blitz-1657512",
    "-titled-tuesday-blitz-1642376",
    "-scc-grand-prix-titled-tuesday-blitz-1613697",
    "-scc-grand-prix-titled-tuesday-blitz-1598916",

    # September 2020
    "-scc-grand-prix-titled-tuesday-blitz-1584634",
    "-scc-grand-prix-titled-tuesday-blitz-1569934",
    "-scc-grand-prix-titled-tuesday-blitz-1569933",
    "-scc-grand-prix-titled-tuesday-blitz-1540597",
    "-scc-grand-prix-titled-tuesday-blitz-1540596",

    # August 2020
    "-scc-grand-prix-titled-tuesday-blitz-1526407",
    "-scc-grand-prix-titled-tuesday-blitz-1496673",
    "-scc-grand-prix-titled-tuesday-blitz-1496670",
    "-scc-grand-prix-titled-tuesday-blitz-1471954",

    # JUly 2020
    "-scc-grand-prix-titled-tuesday-blitz-1331040",
    "-scc-grand-prix-titled-tuesday-blitz-1314461",
    "-scc-grand-prix-titled-tuesday-blitz-1308796",

    # June 2020
    "-scc-grand-prix-titled-tuesday-blitz-1293512",
    "-scc-grand-prix-titled-tuesday-blitz-1287259",
    "-scc-grand-prix-titled-tuesday-blitz-1259839",
    "-scc-grand-prix-titled-tuesday-blitz-1253603",
    "-scc-grand-prix-titled-tuesday-blitz-1246996",

    # May 2020
    "-titled-tuesday-blitz-1240807",
    "-titled-tuesday-blitz-1233743",
    "-titled-tuesday-blitz-1225223",
    "-titled-tuesday-blitz-1213181",

    # April 2020
    "-titled-tuesday-blitz-1208093",
    "-titled-tuesday-blitz-1199696",
    "-titled-tuesday-blitz-1189334",
    "-titled-tuesday-blitz-1182433",

    # March 2020
    "-titled-tuesday-blitz-1152628",
    "-titled-tuesday-blitz-1152623",

    # February 2020
    "-titled-tuesday-blitz-1144554",
    "-titled-tuesday-blitz-1144553",

    # January 2020
    "-titled-tuesday-blitz-1136499",
    "-titled-tuesday-blitz-am-1136500",

    # 2019 titled tuesdays
    "2019-chess-com-daily-chess-championship",
    "-titled-tuesday-blitz-1125173",
    "-titled-tuesday-blitz-1117830",
    "-titled-tuesday-blitz-1105893",
    "-titled-tuesday-blitz-1097711",
    "-titled-tuesday-blitz-1089335",
    "-titled-tuesday-blitz-1078636",
    "-titled-tuesday-blitz-1070427",
    "-titled-tuesday-blitz-1061838",
    "-titled-tuesday-blitz-1051389",
    "-titled-tuesday-blitz-1042665",
    "-titled-tuesday-blitz-1034328",
    "-titled-tuesday-blitz-1024163"
]

