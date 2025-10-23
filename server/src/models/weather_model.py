"""
Weather model definition for SQLAlchemy ORM.
This model represents weather data stored in PostgreSQL.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from server.src.db.base import Base


class Weather(Base):
    """SQLAlchemy model for storing weather information."""

    __tablename__ = "weather"
    __table_args__ = {"extend_existing": True} 

    id: int = Column(Integer, primary_key=True, index=True)
    city: str = Column(String(50), nullable=False, index=True)
    temperature: float = Column(Float, nullable=False)
    description: str = Column(String(100), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Weather(city={self.city}, temp={self.temperature})>"
