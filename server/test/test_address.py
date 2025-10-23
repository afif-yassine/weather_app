# server/test/test_address.py
from server.test.conftest import client

def test_add_address(test_user, address_data):
    response = client.post("/addresses/", params={"user_id": test_user.id}, json=address_data)
    assert response.status_code == 200
    data = response.json()
    assert data["street"] == address_data["street"]
    assert data["user_id"] == test_user.id

def test_list_addresses(test_user, address_data):
    client.post("/addresses/", params={"user_id": test_user.id}, json=address_data)
    response = client.get("/addresses/", params={"user_id": test_user.id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["user_id"] == test_user.id
    assert data[0]["street"] == address_data["street"]

def test_list_no_addresses():
    response = client.get("/addresses/", params={"user_id": 9999})
    assert response.status_code == 404
    assert response.json()["detail"] == "No addresses found"
