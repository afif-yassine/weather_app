# services/history_service.py
from sqlalchemy.orm import Session
from server.src.models.history_model import History
from server.src.models.user_model import User
from server.src.models.activity_model import Activity
from datetime import datetime

def add_to_history(user: User, activity: Activity, db: Session):
    """
    Ajoute une activité à l'historique de l'utilisateur.
    """
    # Vérifier si déjà dans l'historique
    existing = db.query(History).filter_by(user_id=user.id, activity_id=activity.id).first()
    if not existing:
        history_entry = History(user_id=user.id, activity_id=activity.id)
        db.add(history_entry)
        db.commit()
        db.refresh(history_entry)
        return history_entry
    return existing

def get_user_history(user: User, db: Session):
    """
    Retourne l'historique des activités vues par l'utilisateur.
    """
    return db.query(History).filter_by(user_id=user.id).order_by(History.timestamp.desc()).all()
