from sqlalchemy import (
    Column, Integer, String, Boolean, Enum, Float, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from server.src.db.base import Base
import enum
from datetime import datetime

# ------------------ ENUMS ------------------

class IntensityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class WeatherConditionEnum(str, enum.Enum):
    sunny = "sunny"
    rainy = "rainy"
    cloudy = "cloudy"
    snowy = "snowy"
    windy = "windy"
    foggy = "foggy"
    stormy = "stormy"

class LocationTypeEnum(str, enum.Enum):
    indoor = "indoor"
    outdoor = "outdoor"
    mixed = "mixed"

class AccessibilityLevelEnum(str, enum.Enum):
    easy = "easy"
    moderate = "moderate"
    hard = "hard"

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

    ########!!!
    session_id = Column(String, index=True, nullable=True)  
    ########!!!
    
    categories = relationship("Category", secondary=activity_category, back_populates="activities")
    tags = relationship("Tag", secondary=activity_tag, back_populates="activities")

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


# ------------------ Pydantic Schemas ------------------
from pydantic import BaseModel
from typing import List, Optional

# For output (full objects)
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

class ActivityOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_outdoor: Optional[bool]
    is_groupe: Optional[bool]
    intensity: Optional[IntensityEnum]
    duration: Optional[float]
    ideal_temperature_min: Optional[float]
    ideal_temperature_max: Optional[float]
    weather_conditions: Optional[WeatherConditionEnum]
    location_type: Optional[LocationTypeEnum]
    min_age: Optional[int]
    max_age: Optional[int]
    accessibility_level: Optional[AccessibilityLevelEnum]
    categories: Optional[List[CategoryOut]] = []
    tags: Optional[List[TagOut]] = []

    class Config:
        orm_mode = True

# For input (only IDs for categories/tags)
class ActivityCreate(BaseModel):
    name: str
    description: Optional[str]
    is_outdoor: Optional[bool]
    is_groupe: Optional[bool]
    intensity: Optional[IntensityEnum]
    duration: Optional[float]
    ideal_temperature_min: Optional[float]
    ideal_temperature_max: Optional[float]
    weather_conditions: Optional[WeatherConditionEnum]
    location_type: Optional[LocationTypeEnum]
    min_age: Optional[int]
    max_age: Optional[int]
    accessibility_level: Optional[AccessibilityLevelEnum]
    categories: Optional[List[int]] = []
    tags: Optional[List[int]] = []