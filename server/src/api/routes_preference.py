from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.src.db.base import get_db
from server.src.middlewares.auth_middleware import get_current_user_from_db, require_role
from server.src.schemas.preference_schema import BallotCreate, SessionAttachByIds
from server.src.services.preference_service import create_ballot, attach_session_by_ids, compute_condorcet_winner

router = APIRouter(prefix="/preferences", tags=["preferences"])

# 🧑‍💼 Admin : créer les activités d'une session
AdminOnly = require_role([2])  # remplace 1 par l’ID réel de ton rôle admin

@router.post("/attach-by-ids")
def create_session_with_existing_activities(
    payload: SessionAttachByIds,
    db: Session = Depends(get_db),
    admin = Depends(AdminOnly),
):
    return attach_session_by_ids(db, payload.session_id, payload.activity_ids)

# 👥 Utilisateur : voter
@router.post("/ballots")
def vote(payload: BallotCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user_from_db)):
    ballot = create_ballot(db, current_user.id, payload.session_id, [r.dict() for r in payload.rankings])
    return {"ballot_id": ballot.id, "message": "Vote enregistré avec succès."}

# ⚙️ Calculer le vainqueur Condorcet
@router.post("/condorcet/{session_id}")
def condorcet(session_id: str, db: Session = Depends(get_db)):
    return compute_condorcet_winner(db, session_id)
