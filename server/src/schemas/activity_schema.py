from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import enum
from server.src.enums.activity_enums import IntensityEnum, WeatherConditionEnum, LocationTypeEnum, AccessibilityLevelEnum


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


# ----------------------------
# Category and Tag Schemas
# ----------------------------
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str
    description: Optional[str] = None

class Tag(TagBase):
    id: int
    class Config:
        orm_mode = True


# ----------------------------
# Activity Schemas
# ----------------------------
class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_outdoor: Optional[bool] = None
    is_groupe: Optional[bool] = None
    intensity: Optional[IntensityEnum] = None
    duration: Optional[float] = None
    ideal_temperature_min: Optional[float] = None
    ideal_temperature_max: Optional[float] = None
    weather_conditions: Optional[WeatherConditionEnum] = None
    location_type: Optional[LocationTypeEnum] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    accessibility_level: Optional[AccessibilityLevelEnum] = None
    categories: Optional[List[int]] = []
    tags: Optional[List[int]] = []


# ✅ The input payload expects lists of IDs, not objects
class ActivityCreate(ActivityBase):
    categories: Optional[List[int]] = []
    tags: Optional[List[int]] = []


# For reading from DB (response)
class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    categories: List[Category] = []
    tags: List[Tag] = []

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
    categories: Optional[List[Category]] = []
    tags: Optional[List[Tag]] = []

    class Config:
        orm_mode = True

# For input (only IDs for categories/tags)