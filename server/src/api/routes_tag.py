from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.src.db.base import SessionLocal
from server.src.models.activity_model import TagOut
from server.src.services.tag_service import get_tags, get_tag, create_tag, update_tag, delete_tag
from server.src.middlewares.auth_middleware import require_role

router = APIRouter(prefix="/tags", tags=["tags"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return get_tags(db)

@router.get("/{tag_id}", response_model=TagOut)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.post("/", response_model=TagOut)
def create_new_tag(name: str, description: str = None, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    return create_tag(db, name, description)

@router.put("/{tag_id}", response_model=TagOut)
def update_existing_tag(tag_id: int, name: str = None, description: str = None, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    tag = update_tag(db, tag_id, name, description)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.delete("/{tag_id}", response_model=TagOut)
def delete_existing_tag(tag_id: int, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    tag = delete_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
