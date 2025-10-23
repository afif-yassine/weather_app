from sqlalchemy.orm import Session
from server.src.models.activity_model import Activity, Category, Tag
from server.src.schemas.activity_schema import ActivityCreate
from typing import List

def get_activities(db: Session) -> List[Activity]:
    return db.query(Activity).all()

def get_activity(db: Session, activity_id: int) -> Activity:
    return db.query(Activity).filter(Activity.id == activity_id).first()

def create_activity(db: Session, activity: ActivityCreate) -> Activity:
    db_activity = Activity(
        name=activity.name,
        description=activity.description,
        is_outdoor=activity.is_outdoor,
        is_groupe=activity.is_groupe,
        intensity=activity.intensity,
        duration=activity.duration,
        ideal_temperature_min=activity.ideal_temperature_min,
        ideal_temperature_max=activity.ideal_temperature_max,
        weather_conditions=activity.weather_conditions,
        location_type=activity.location_type,
        min_age=activity.min_age,
        max_age=activity.max_age,
        accessibility_level=activity.accessibility_level,
    )
    # Assign categories by IDs
    if activity.categories:
        db_activity.categories = db.query(Category).filter(Category.id.in_(activity.categories)).all()
    # Assign tags by IDs
    if activity.tags:
        db_activity.tags = db.query(Tag).filter(Tag.id.in_(activity.tags)).all()
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity
