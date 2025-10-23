from sqlalchemy.orm import Session
from server.src.models.activity_model import Tag
from typing import List

def get_tags(db: Session) -> List[Tag]:
    return db.query(Tag).all()

def get_tag(db: Session, tag_id: int) -> Tag:
    return db.query(Tag).filter(Tag.id == tag_id).first()

def create_tag(db: Session, name: str, description: str = None) -> Tag:
    db_tag = Tag(name=name, description=description)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, tag_id: int, name: str = None, description: str = None) -> Tag:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    if name is not None:
        db_tag.name = name
    if description is not None:
        db_tag.description = description
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int) -> Tag:
    db_tag = get_tag(db, tag_id)
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag
