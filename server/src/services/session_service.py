# services/session_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from server.src.models.activity_model import Activity

def attach_session_by_ids(db: Session, session_id: str, activity_ids: list[int]) -> dict:
    if not activity_ids:
        raise HTTPException(400, "activity_ids vide")

    acts = db.query(Activity).filter(Activity.id.in_(activity_ids)).all()
    if len(acts) != len(set(activity_ids)):
        missing = sorted(set(activity_ids) - {a.id for a in acts})
        raise HTTPException(400, f"Activité(s) inexistante(s): {missing}")

    # (Optionnel) Empêcher qu'une activité soit déjà dans une autre session
    clash = [a for a in acts if a.session_id and a.session_id != session_id]
    if clash:
        raise HTTPException(409, {
            "already_in_other_session": [{"id": a.id, "session_id": a.session_id} for a in clash]
        })

    for a in acts:
        a.session_id = session_id
    db.commit()

    return {"session_id": session_id, "attached_ids": [a.id for a in acts], "count": len(acts)}
