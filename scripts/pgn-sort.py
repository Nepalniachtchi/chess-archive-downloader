import os
import sys
from pgn.sorter import PgnSorter
from config import PGN_ROOT

# print("[ARG]", sys.argv)

if len(sys.argv) < 3:
    raise Exception("missing args: pgn-sort.py INPUT OUTPUT")

input_file = sys.argv[1]
output_file = sys.argv[2]

# input_file = os.path.join(PGN_ROOT, "A54-budapest-5-Bf4.pgn")
# output_file = os.path.join(PGN_ROOT, "A54-budapest-5-Bf4-sorted.pgn")
# input_file = os.path.join(PGN_ROOT, "chesscom-elite-2021-07.pgn")


sorter = PgnSorter()

sorter \
    .set_input_file(input_file) \
    .set_output_file(output_file) \
    .sort()
