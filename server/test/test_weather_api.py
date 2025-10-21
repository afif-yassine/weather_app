"""
Pytest tests for Weather API routes using HTTPX.
"""

import pytest
from fastapi.testclient import TestClient
from server.src.main import app

client = TestClient(app)


@pytest.fixture
def example_weather():
    return {"city": "Paris", "temperature": 22.5, "description": "Sunny"}


def test_create_weather(example_weather):
    """Test creating a weather record."""
    response = client.post("/weather/", json=example_weather)
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Paris"
    assert "id" in data


def test_list_weather():
    """Test retrieving weather records."""
    response = client.get("/weather/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
