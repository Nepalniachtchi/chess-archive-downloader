from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class TournamentPlayer(BaseModel):
    username: str
    rating_hi: Optional[int]
    rating_lo: Optional[int]
    points: Optional[str]

class Tournament(BaseModel):
    id: str
    name: str
    url: str
    status: str
    start_time: date
    end_time: Optional[date]

    # Tournament settings
    time_class: str
    time_control: str
    type: str
    rules: str
    is_rated: bool
    is_official: bool
    is_invite_only: bool
    total_rounds: int

    players: List[TournamentPlayer]
