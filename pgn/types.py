from enum import Enum
from pydantic import BaseModel


class PgnBlockType(Enum):
    HEAD = "HEAD"
    BODY = "BODY"
    NONE = None


class PgnBlock(BaseModel):
    type: PgnBlockType
    offset: int
    length: int
    text: str
