from sqlalchemy.orm import Session
from server.src.models.user_model import User
from server.src.models.role_model import Role
from server.src.core.security import get_password_hash, verify_password, decode_token, create_access_token, create_refresh_token
from server.src.schemas.auth_schema import Token
from datetime import timedelta
from server.src.schemas.user_schema import UserResponse
from server.src.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
def register_user(db: Session, email: str, username: str, password: str, role_id: int):
    hashed_pw = get_password_hash(password)
    
    role_obj = db.query(Role).filter(Role.id == role_id).first()
    if not role_obj:
        raise ValueError(f"Le rôle avec id {role_id} n'existe pas")

    # Crée l'utilisateur avec role_id au lieu de l'objet complet
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_pw,
        role_id=role_obj.id  # ✅ juste l'ID
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    # Préparer la réponse Pydantic
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        role_id=user.role_id
    )

    return user_response


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return Token(access_token=access_token, refresh_token=refresh_token)

def verify_and_create_new_access_token(refresh_token: str, db: Session):
    payload = decode_token(refresh_token, refresh=True)
    if not payload:
        return None

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        return None

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return Token(access_token=access_token, refresh_token=refresh_token)