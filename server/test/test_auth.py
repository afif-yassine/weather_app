# server/test/test_auth.py
import random
from server.src.db.base import get_db
from server.src.models.role_model import Role


def _db_from_client(client):
    # open a DB session using the app's dependency override
    db_gen = client.app.dependency_overrides[get_db]()
    db = next(db_gen)
    return db, db_gen


def _close_db_gen(db_gen):
    try:
        next(db_gen)
    except StopIteration:
        pass


def test_register_user(client_user):
    db, db_gen = _db_from_client(client_user)
    try:
        user_role = db.query(Role).filter(Role.name == "user").first()
        assert user_role is not None
        role_id = user_role.id
    finally:
        _close_db_gen(db_gen)

    resp = client_user.post(
        "/auth/register",
        json={
            "email": f"newuser{random.randint(1,10000)}@example.com",
            "username": f"newuser{random.randint(1,10000)}",
            "password": "Test123!",
            "age": 30,
            "sexe": "male",
            "role_id": role_id,
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["role_id"] == role_id


def test_login_user(client_user, test_user):
    resp = client_user.post(
        "/auth/login",
        json={
            "email": test_user.email,
            "password": "Test123!",
        },
    )
    assert resp.status_code == 200, resp.text
    tokens = resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_login_invalid_user(client_user):
    resp = client_user.post(
        "/auth/login", json={"email": "fake@example.com", "password": "nopass"}
    )
    assert resp.status_code in (400, 401), resp.text
