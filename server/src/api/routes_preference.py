from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.src.db.base import get_db
from server.src.middlewares.auth_middleware import get_current_user_from_db
from server.src.schemas.preference_schema import BallotCreate
from server.src.services.preference_service import create_ballot, compute_condorcet_winner

router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.post("/ballots")
def post_ballot(payload: BallotCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user_from_db)):
    ballot = create_ballot(
        db,
        user_id=current_user.id,
        session_id=payload.session_id,
        rankings=[r.dict() for r in payload.rankings]
    )
    return {"ballot_id": ballot.id, "session_id": payload.session_id}


@router.get("/condorcet/{session_id}")
def get_condorcet(session_id: str, db: Session = Depends(get_db)):
    """
    Exemple: /preferences/condorcet/pack_1234
    """
    result = compute_condorcet_winner(db, session_id)
    return result
