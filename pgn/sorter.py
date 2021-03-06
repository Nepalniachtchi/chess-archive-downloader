import os
import re
from pydantic import BaseModel
from pgn.types import PgnBlock, PgnBlockType
from pgn.game import PgnGame

SIZE_64KB: int = 1024 * 64
SIZE_1MB: int = 1024 * 1024

DEFAULT_CHUNK_SIZE: int = 10000

EMPTY_STRING: str = ""
PGN_BLOCK_SEPARATOR: str = "\n\n"
PGN_HEADER_PREFIX: str = "["
PGN_HEADER_REGEX: str = r'^(\[\w+ "[^"]+"]\s)+(\[\w+ "[^"]+"])$'

PGN_BLOCK_SEPARATOR_LENGTH: int = len(PGN_BLOCK_SEPARATOR)


class TextChunk(BaseModel):
    offset: int
    length: int
    text: str


def each_chunk(input_file, chunk_size=DEFAULT_CHUNK_SIZE):
    offset = 0
    with open(input_file, "r") as input_file:
        while True:
            data = input_file.read(chunk_size)
            if not data:
                break
            length = len(data)
            # print(f"[CHUNK] [{offset}->{offset+length-1}] Read in {length} bytes")
            yield TextChunk(
                offset=offset,
                length=length,
                text=data
            )
            offset += length


def each_pgn_block(input_file):
    left_over = EMPTY_STRING
    for chunk in each_chunk(input_file):
        offset = chunk.offset - len(left_over)
        chunk = left_over + chunk.text
        left_over = EMPTY_STRING

        blocks = chunk.split(PGN_BLOCK_SEPARATOR)

        if blocks[-1] != EMPTY_STRING:
            left_over = blocks.pop()

        # print(f"[BLOCK] Have {len(blocks)} Blocks")
        for block in blocks:
            length = len(block) + PGN_BLOCK_SEPARATOR_LENGTH
            # print(f"[BLOCK] [{offset}->{offset+length-1}] Block size: {length} bytes")
            is_pgn_header = (
                block
                and block.startswith(PGN_HEADER_PREFIX)
                and re.match(PGN_HEADER_REGEX, block)
            )
            block_type: PgnBlockType = (
                PgnBlockType.HEAD if is_pgn_header
                else PgnBlockType.BODY if block
                else PgnBlockType.NONE
            )
            yield PgnBlock(
                type=block_type,
                offset=offset,
                length=length,
                text=block
            )
            offset += length


def each_pgn_game(input_file):
    game_count = 0
    game = None
    for block in each_pgn_block(input_file):
        if not block:
            break
        # print(f"[BLOCK] {block.length}: {block.type} >>>\n{block.text}\n<<<<<<---<<<<<<---")
        # print(f"[BLOCK] {block.type}: {block.length} bytes")
        if block.type == PgnBlockType.HEAD:
            if game is not None:
                yield game
            game_count += 1
            game = PgnGame(game_count)
            # print("[PGN] Add Header")
            game.add_header(block)
        else:
            # print("[PGN] Add Body")
            game.add_body(block)

def end_date_sort_key(pgn_headers):
    return f"{pgn_headers['EndDate']}T{pgn_headers['EndTime']}"

def date_sort_key(pgn_headers):
    return f"{pgn_headers['Date']}{pgn_headers['Round'].ljust(4, '0')}"

class PgnSorter():
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.sort_fields = []
        self.items = []

    def set_input_file(self, input_file):
        self.input_file = input_file
        return self

    def set_output_file(self, output_file):
        self.output_file = output_file
        return self

    def sort_by_header(self, header: str):
        self.sort_fields = [header]
        return self

    def sort(self):
        print(f"[SORT] Reading input file {os.path.basename(self.input_file)}")
        for game in each_pgn_game(self.input_file):
            # print(f"[{game.game_no:07}] {game}")
            # sort_key = end_date_sort_key(game.get_headers())
            sort_key = end_date_sort_key(game.get_headers())
            self.items.append({
                "key": sort_key,
                "data": game,
            })

        print(f"[SORT] sorting ({len(self.items)} items)")
        # sorted_list = sorted(self.items, key=lambda k: k['key'])
        self.items.sort(key=lambda k: k['key'])

        print(f"[SORT] Writing output file {os.path.basename(self.output_file)}")
        with open(self.output_file, "w") as output_file:
            for item in self.items:
                buffer = [block.text for block in item["data"].blocks]
                output_file.write(PGN_BLOCK_SEPARATOR.join(buffer))

        print(f"[SORT] sort complete.")
