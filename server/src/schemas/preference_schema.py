from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional

class RankIn(BaseModel):
    activity_id: int
    rank: int

class BallotCreate(BaseModel):
    context_date: Optional[date] = None   # ⬅️ date (YYYY-MM-DD)
    rankings: List[RankIn]

class BallotOut(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
