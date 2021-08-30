import os
from pgn.sorter import PgnSorter
from config import PGN_ROOT

# input_file = os.path.join(PGN_ROOT, "A54-budapest-5-Bf4.pgn")
input_file = os.path.join(PGN_ROOT, "chesscom-elite-2021-07.pgn")
output_file = "sorted.pgn"


sorter = PgnSorter()

sorter \
    .set_input_file(input_file) \
    .sort()
