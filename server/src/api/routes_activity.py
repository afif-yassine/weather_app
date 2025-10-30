from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.src.db.base import SessionLocal
from server.src.schemas.activity_schema import Activity, ActivityCreate, ActivityOut
from server.src.services.activity_service import get_activities, get_activity, create_activity, delete_activity
from server.src.middlewares.auth_middleware import require_role

router = APIRouter(prefix="/activities", tags=["activities"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    return get_activities(db)

@router.get("/{activity_id}", response_model=ActivityOut)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.post("/", response_model=ActivityOut)
def create_new_activity(activity: ActivityCreate, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    return create_activity(db, activity)

@router.delete("/{activity_id}", response_model=ActivityOut)
def delete_existing_activity(activity_id: int, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    activity = delete_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(activity_id: int, activity: ActivityCreate, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    for field, value in activity.dict(exclude_unset=True).items():
        setattr(db_activity, field, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity
