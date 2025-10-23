from fastapi import APIRouter, Depends, HTTPException, status, Header, Path
from sqlalchemy.orm import Session

from server.src.db.base import get_db
from server.src.schemas.user_schema import UserCreate, UserResponse
from server.src.schemas.auth_schema import Token, LoginRequest
from server.src.services.auth_service import (
    register_user,
    authenticate_user,
    deactivate_user,
    verify_and_create_new_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentification"])

# -----------------------------
# 🚀 Public endpoints (pas de JWT)
# -----------------------------
@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur
    - role_id doit être fourni dans UserCreate
    """
    user = register_user(
        db, 
        email=data.email, 
        username=data.username, 
        age=data.age,
        sexe=data.sexe,
        password=data.password, 
        role_id=data.role_id
    )
    return user


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authentifie un utilisateur et renvoie un access & refresh token
    """
    token = authenticate_user(db, data.email, data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    return token


# -----------------------------
# 🔄 Refresh token (public, nécessite seulement le refresh token)
# -----------------------------
@router.post("/refresh-token", response_model=Token)
def refresh_token_endpoint(
    refresh_token: str = Header(...), 
    db: Session = Depends(get_db)
):
    """
    Vérifie le refresh token et crée un nouveau access token
    """
    new_token = verify_and_create_new_access_token(refresh_token, db)
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh token"
        )
    return new_token

# -----------------------------
# 🚫 Désactiver un utilisateur
# -----------------------------
@router.patch("/deactivate/{user_id}", response_model=UserResponse)
def deactivate_user_endpoint(
    user_id: int = Path(..., description="ID de l'utilisateur à désactiver"),
    db: Session = Depends(get_db)
):
    """
    Désactive un utilisateur (is_active = False)
    """
    try:
        user_data = deactivate_user(db, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return user_data
