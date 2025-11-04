from pydantic import BaseModel, Field
from typing import List, Optional

class RankIn(BaseModel):
    activity_id: int
    rank: int

class BallotCreate(BaseModel):
    session_id: str
    rankings: List[RankIn]

class ActivityCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SessionActivitiesCreate(BaseModel):
    session_id: str
    activities: List[ActivityCreate]

class SessionAttachByIds(BaseModel):
    session_id: str = Field(..., examples=["pack_911"])
    activity_ids: List[int] = Field(..., min_items=2, examples=[[1,2,3,4]])