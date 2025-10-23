# server/test/test_auth.py
import random
from server.test.conftest import client, override_get_db
from server.src.models.role_model import Role

def test_register_user():
    db = next(override_get_db())
    user_role = db.query(Role).filter(Role.name == "user").first()
    response = client.post("/auth/register", json={
        "email": f"newuser{random.randint(1,10000)}@example.com",
        "username": f"newuser{random.randint(1,10000)}",
        "password": "Test123!",
        "role_id": user_role.id,
        "age": 30,
        "sexe": "male"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["role_id"] == user_role.id

def test_login_user(test_user):
    response = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "Test123!"
    })
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

def test_login_invalid_user():
    response = client.post("/auth/login", json={"email": "fake@example.com", "password": "nopass"})
    assert response.status_code == 401
