from pydantic import BaseModel, ConfigDict
from typing import List

class RankIn(BaseModel):
    activity_id: int
    rank: int

class BallotCreate(BaseModel):
    session_id: str  # identifiant unique de la session
    rankings: List[RankIn]  # liste des choix ordonnés

class BallotOut(BaseModel):
    id: int
    session_id: str
    model_config = ConfigDict(from_attributes=True)
