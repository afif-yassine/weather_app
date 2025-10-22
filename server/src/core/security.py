# server/src/core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from server.src.core.config import (
    SECRET_KEY_ACCESS,
    SECRET_KEY_REFRESH,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)

# -----------------------------
# 🔐 Gestion des mots de passe
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password: str) -> str:
    truncated_pw = password[:72]
    return pwd_context.hash(truncated_pw)

# -----------------------------
# 🕒 Création & décodage JWT
# -----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_ACCESS, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)

def decode_token(token: str, refresh: bool = False):
    secret = SECRET_KEY_REFRESH if refresh else SECRET_KEY_ACCESS
    try:
        return jwt.decode(token, secret, algorithms=[ALGORITHM])
    except JWTError:
        return None
