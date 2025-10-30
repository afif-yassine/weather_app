from sqlalchemy import (
    Column, Integer, String, Boolean, Enum, Float, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from server.src.db.base import Base
from .history_model import History
from datetime import datetime
from server.src.enums.activity_enums import IntensityEnum, WeatherConditionEnum, LocationTypeEnum, AccessibilityLevelEnum

# ------------------ ASSOCIATION TABLES ------------------
activity_category = Table(
    "activity_category",
    Base.metadata,
    Column("activity_id", Integer, ForeignKey("activity.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)

activity_tag = Table(
    "activity_tag",
    Base.metadata,
    Column("activity_id", Integer, ForeignKey("activity.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True),
)

# ------------------ SQLALCHEMY MODELS ------------------

class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_outdoor = Column(Boolean, nullable=True)
    is_groupe = Column(Boolean, nullable=True)
    intensity = Column(Enum(IntensityEnum, native_enum=False), nullable=True)
    duration = Column(Float, nullable=True)
    ideal_temperature_min = Column(Float, nullable=True)
    ideal_temperature_max = Column(Float, nullable=True)
    weather_conditions = Column(Enum(WeatherConditionEnum, native_enum=False), nullable=True)
    location_type = Column(Enum(LocationTypeEnum, native_enum=False), nullable=True)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    accessibility_level = Column(Enum(AccessibilityLevelEnum, native_enum=False), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("Category", secondary=activity_category, back_populates="activities")
    tags = relationship("Tag", secondary=activity_tag, back_populates="activities")
    history = relationship("History", back_populates="activity", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    activities = relationship("Activity", secondary=activity_category, back_populates="categories")

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    activities = relationship("Activity", secondary=activity_tag, back_populates="tags")

from pydantic import BaseModel
from typing import List, Optional

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class TagOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
