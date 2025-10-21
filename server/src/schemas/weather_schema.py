"""
Pydantic schemas for weather API input/output validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WeatherBase(BaseModel):
    city: str = Field(..., example="Paris")
    temperature: float = Field(..., example=18.5)
    description: Optional[str] = Field(None, example="Cloudy")


class WeatherCreate(WeatherBase):
    """Schema for creating a weather record."""
    pass


class WeatherResponse(WeatherBase):
    """Schema for returning weather record from API."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
