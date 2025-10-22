from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from server.src.core.security import decode_token
from server.src.db.base import SessionLocal, get_db
from server.src.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -----------------------------
# 👤 Récupération de l'utilisateur courant depuis le token JWT
# -----------------------------
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Récupère l'utilisateur à partir du token JWT.
    Retourne un dict contenant 'sub' (email) et éventuellement 'role'.
    """
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# -----------------------------
# 👤 Récupération de l'utilisateur depuis la base de données
# -----------------------------
def get_current_user_from_db(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Récupère l'objet User SQLAlchemy correspondant au token JWT.
    Utile pour vérifier le rôle avec require_role.
    """
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
        )

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    return user


# -----------------------------
# 🧩 Vérification du rôle
# -----------------------------
def require_role(required_roles: list[int]):
    """
    Dépendance pour protéger les routes selon le rôle.
    `required_roles` : liste des rôles autorisés (ex: [1, 2])
    """
    def role_checker(user: User = Depends(get_current_user_from_db)):
        if user.role_id not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé – rôle insuffisant",
            )
        return user
    return role_checker


# -----------------------------
# 🌐 Middleware global pour JWT (optionnel)
# -----------------------------
async def jwt_middleware(request: Request, call_next):
    """
    Middleware pour vérifier le token sur toutes les routes sauf /auth/*
    Stocke le payload JWT dans request.state.user
    """
    if request.url.path.startswith("/auth"):
        return await call_next(request)

    authorization: str = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token manquant"},
        )

    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if payload is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token invalide ou expiré"},
        )

    request.state.user = payload
    return await call_next(request)
