# server/test/test_address.py


AUTH_USER_ID = 101  # matches FakeUser in conftest


def test_add_address(client_user, test_user, address_data):
    resp = client_user.post(
        "/addresses/", params={"user_id": test_user.id}, json=address_data
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["street"] == address_data["street"]
    # API uses current_user, not the query param
    assert data["user_id"] == AUTH_USER_ID


def test_list_addresses(client_user, test_user, address_data):
    client_user.post("/addresses/", params={"user_id": test_user.id}, json=address_data)
    resp = client_user.get("/addresses/", params={"user_id": test_user.id})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["street"] == address_data["street"]
    assert data[0]["user_id"] == AUTH_USER_ID


def test_list_no_addresses(client_user):
    resp = client_user.get("/addresses/", params={"user_id": 9999})
    # Your API may return 404 or 200 with an empty list—accept both
    assert resp.status_code in (200, 404), resp.text
    if resp.status_code == 404:
        assert resp.json().get("detail") in ("No addresses found", "Not Found")
