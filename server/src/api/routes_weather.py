"""
Weather API routes.
Provide endpoints to create and list weather data.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.src.db.base import SessionLocal
from server.src.schemas.weather_schema import WeatherCreate, WeatherResponse
from server.src.models.weather_model import Weather
from server.src.services.weatherApi import fetch_forecast_by_date

router = APIRouter(prefix="/weather", tags=["Weather"])

def get_db():
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=WeatherResponse, summary="Add new weather data", response_description="The created weather record.")
def add_weather(weather: WeatherCreate, db: Session = Depends(get_db)) -> WeatherResponse:
    """
    Create a new weather entry in the database.

    - **city**: name of the city
    - **temperature**: current temperature
    - **description**: optional weather description
    """
    record = Weather(**weather.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[WeatherResponse], summary="List all weather data", response_description="List of weather records.")
def list_weather(db: Session = Depends(get_db)) -> list[WeatherResponse]:
    """Return all weather entries in the database."""
    return db.query(Weather).all()


@router.get("/forecast/{city}/{date}")
def get_forecast_by_date(city: str, date: str):
    """
    Example: GET /forecast/Paris/2024-10-20
    """
    try:
        result = fetch_forecast_by_date(city=city, date=date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))