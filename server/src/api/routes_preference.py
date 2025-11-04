from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from server.src.db.base import get_db
from server.src.middlewares.auth_middleware import get_current_user_from_db
from server.src.schemas.preference_schema import BallotCreate
from server.src.services.preference_service import create_ballot, compute_condorcet_winner

router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.post("/ballots")
def post_ballot(
    payload: BallotCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_db),
):
    ballot = create_ballot(
        db,
        user_id=current_user.id,
        rankings=[r.dict() for r in payload.rankings],
        context_date=payload.context_date,
    )
    return {"ballot_id": ballot.id}

@router.post("/condorcet")
def condorcet(
    activity_ids: list[int] = Body(..., example=[1, 5, 7]),
    db: Session = Depends(get_db),
):
    return compute_condorcet_winner(db, activity_ids)
