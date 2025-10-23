from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.src.db.base import SessionLocal
from server.src.models.activity_model import CategoryOut
from server.src.services.category_service import get_categories, get_category, create_category, update_category, delete_category
from server.src.middlewares.auth_middleware import require_role

router = APIRouter(prefix="/categories", tags=["categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@router.get("/{category_id}", response_model=CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryOut)
def create_new_category(name: str, description: str = None, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    return create_category(db, name, description)

@router.put("/{category_id}", response_model=CategoryOut)
def update_existing_category(category_id: int, name: str = None, description: str = None, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    category = update_category(db, category_id, name, description)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", response_model=CategoryOut)
def delete_existing_category(category_id: int, db: Session = Depends(get_db), user: dict = Depends(require_role([2]))):
    category = delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
