# server/test/test_activity.py
import random
import pytest
from server.test.conftest import client, override_get_db
from server.src.models.activity_model import Activity, Category, Tag
from datetime import datetime

pytestmark = pytest.mark.django_db


def test_create_activity():
    db = next(override_get_db())

    # create category + tag first (normally this is done in fixtures or migrations)
    cat = Category(name=f"cat{random.randint(1,10000)}")
    db.add(cat)

    tag = Tag(name=f"tag{random.randint(1,10000)}")
    db.add(tag)
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
        "location_type": "field",
        "min_age": 10,
        "max_age": 50,
        "accessibility_level": "normal",
        "category_ids": [cat.id],
        "tag_ids": [tag.id]
    }

    resp = client.post("/activities/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == payload["name"]
    assert len(data["categories"]) == 1
    assert len(data["tags"]) == 1


def test_get_activities_list():
    resp = client.get("/activities/")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    # pagination aware (if u return results) OR direct list (if yours returns list)
    # but this keeps same style as ur auth tests
