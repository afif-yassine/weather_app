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

# ⬇️ NEW: import your auth deps so we can override them
from server.src.middlewares.auth_middleware import (
    get_current_user_from_db,
    require_role,
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Keep DB override
app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# Setup tables + rôles
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_db_and_roles():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # seed roles
    for role_name in ["user", "admin"]:
        if not db.query(Role).filter(Role.name == role_name).first():
            db.add(Role(name=role_name))
    db.commit()
    db.close()


# -----------------------------
# Fake principals (users)
# -----------------------------
class FakeUser:
    def __init__(self, user_id: int, role_id: int):
        self.id = user_id
        self.role_id = role_id


# Helper: bind a specific FakeUser to the auth dependency
def make_user_override(fake_user: FakeUser):
    def _dep():
        return fake_user

    return _dep


# Helper: no-op for AdminOnly (if your router stores require_role([2]) into a variable)
def allow_admin_only():
    return True


# -----------------------------
# Clients with identity
# -----------------------------
@pytest.fixture
def client_user():
    # user role_id=1 by convention; adjust if yours differs
    app.dependency_overrides[get_current_user_from_db] = make_user_override(
        FakeUser(101, role_id=1)
    )
    # If your router uses a stored AdminOnly callable, we can also neutralize it here safely:
    try:
        from server.src.api import preferences_router as pr_mod

        app.dependency_overrides[pr_mod.AdminOnly] = allow_admin_only
    except Exception:
        pass
    return TestClient(app)


@pytest.fixture
def client_admin():
    # admin role_id=2
    app.dependency_overrides[get_current_user_from_db] = make_user_override(
        FakeUser(201, role_id=2)
    )
    try:
        from server.src.api import preferences_router as pr_mod

        app.dependency_overrides[pr_mod.AdminOnly] = allow_admin_only
    except Exception:
        pass
    return TestClient(app)


# -----------------------------
# Existing fixtures
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
        sexe="male",
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
        "country": "France",
    }
