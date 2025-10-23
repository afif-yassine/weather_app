# server/test/conftest.py
import pytest
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from server.src.db.base import Base, get_db
from server.src.models.user_model import User
from server.src.models.role_model import Role
from server.src.models.address_model import Address
from server.src.main import app
from server.src.core.security import get_password_hash

# -----------------------------
# Config DB (persistante pour tests)
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # ✅ fichier local
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# -----------------------------
# Setup tables + rôles
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_db_and_roles():
    """Créer toutes les tables et rôles avant les tests"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    for role_name in ["user", "admin"]:
        if not db.query(Role).filter(Role.name == role_name).first():
            db.add(Role(name=role_name))
    db.commit()
    db.close()

# -----------------------------
# Fixtures utilisateur et adresse
# -----------------------------
@pytest.fixture
def test_user():
    db = next(override_get_db())
    user_role = db.query(Role).filter(Role.name == "user").first()
    user = User(
        email=f"user{random.randint(1,10000)}@example.com",
        username=f"user{random.randint(1,10000)}",
        hashed_password=get_password_hash("Test123!"),
        role=user_role,
        age=random.randint(20, 50),
        sexe="male"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def address_data():
    return {
        "street": "123 Main St",
        "city": "Paris",
        "postal_code": "75001",
        "country": "France"
    }
