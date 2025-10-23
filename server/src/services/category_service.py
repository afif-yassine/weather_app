from sqlalchemy.orm import Session
from server.src.models.activity_model import Category
from server.src.models.activity_model import CategoryOut
from typing import List

def get_categories(db: Session) -> List[Category]:
    return db.query(Category).all()

def get_category(db: Session, category_id: int) -> Category:
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db: Session, name: str, description: str = None) -> Category:
    db_category = Category(name=name, description=description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, name: str = None, description: str = None) -> Category:
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    if name is not None:
        db_category.name = name
    if description is not None:
        db_category.description = description
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> Category:
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
