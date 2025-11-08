# server/test/test_activity.py
import random
import pytest
from server.src.models.activity_model import Activity, Category, Tag
from server.test.conftest import override_get_db  # keep if you use it for seeding


def test_create_activity(client_admin):
    db = next(override_get_db())

    cat = Category(name=f"cat{random.randint(1,10000)}")
    tag = Tag(name=f"tag{random.randint(1,10000)}")
    db.add_all([cat, tag])
    db.commit()
    db.refresh(cat)
    db.refresh(tag)

    payload = {
        "name": "Football Match",
        "description": "Test activity",
        "is_outdoor": True,
        "is_groupe": True,
        "intensity": "medium",
        "duration": 90,
        "ideal_temperature_min": 18,
        "ideal_temperature_max": 24,
        "weather_conditions": "sunny",
        "location_type": "outdoor",  # <= was "field"
        "min_age": 10,
        "max_age": 50,
        "accessibility_level": "moderate",  # <= was "normal"
        "category_ids": [cat.id],
        "tag_ids": [tag.id],
    }

    resp = client_admin.post("/activities/", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["name"] == payload["name"]
    assert len(data.get("categories", [])) == 1
    assert len(data.get("tags", [])) == 1


def test_get_activities_list(client_user):
    resp = client_user.get("/activities/")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    # accept list OR paginated dict
    if isinstance(data, dict):
        assert "results" in data
        assert isinstance(data["results"], list)
    else:
        assert isinstance(data, list)
