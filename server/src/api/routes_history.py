# api/routes_history.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.src.db.base import get_db
from server.src.middlewares.auth_middleware import get_current_user_from_db
from server.src.services.history_service import add_to_history, get_user_history
from server.src.models.user_model import User
from server.src.models.activity_model import Activity

router = APIRouter(prefix="/history", tags=["history"])

@router.post("/add/{activity_id}")
def add_activity_to_history(
    activity_id: int,
    current_user: User = Depends(get_current_user_from_db),
    db: Session = Depends(get_db)
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return {"error": "Activity not found"}
    entry = add_to_history(current_user, activity, db)
    return {"message": "Activity added to history", "entry": entry.id}

@router.get("/")
def get_history(
    current_user: User = Depends(get_current_user_from_db),
    db: Session = Depends(get_db)
):
    history = get_user_history(current_user, db)
    return [{"activity_id": h.activity_id, "viewed_at": h.timestamp} for h in history]
