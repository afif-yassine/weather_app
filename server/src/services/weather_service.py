from sqlalchemy.orm import Session
from server.src.models.weather_model import Weather
from server.src.schemas.weather_schema import WeatherCreate

def create_weather(db: Session, weather_data: WeatherCreate):
    weather = Weather(**weather_data.dict())
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather

def get_all_weather(db: Session):
    return db.query(Weather).all()
