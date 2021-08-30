import re
from pgn.types import PgnBlockType
from enum import Enum
from typing import List
from pgn.types import PgnBlock
from pgn.exceptions import PgnLoadingException


PGN_HEADER_REGEX = re.compile('^\[(?P<header>\w+)\s+\"(?P<value>[^\"]+)\"]')


def parse_header_line(header_line: str):
    matches = PGN_HEADER_REGEX.match(header_line)
    return (matches.group("header"), matches.group("value"))


class PgnLoadingState(Enum):
    INIT = "init"
    HEADER = "header"
    BODY = "body"


class PgnGame():
    def __init__(self, game_no: int):
        self.game_no = game_no
        self.blocks: List[PgnBlock] = []
        self.state: PgnLoadingState = PgnLoadingState.INIT

    def add_header(self, header):
        if self.state != PgnLoadingState.INIT:
            raise PgnLoadingException(f"Not expecting a header: {self.state}")

        self.blocks.append(header)
        self.state = PgnLoadingState.HEADER
        
        return self

    def add_body(self, body):
        if self.state not in [PgnLoadingState.HEADER, PgnLoadingState.BODY]:
            raise PgnLoadingException(f"Not expecting a body: {self.state}")

        self.blocks.append(body)
        self.state = PgnLoadingState.BODY

        return self

    def parse_header_block(self, block):
        lines = block.text.split("\n")
        return dict(parse_header_line(line) for line in lines)

    def short_header(self):
        headers = self.parse_header_block(self.blocks[0])
        players = f"{headers['White']} - {headers['Black']}".ljust(46)[:46]
        event = headers['Event'].ljust(20)[:20]
        year = headers['Date'][:4]
        result = headers['Result'][:3]
        return (
            f"{players} {event}"
            f" {year} {result}"
        )
    
    def __repr__(self):
        return self.short_header()
