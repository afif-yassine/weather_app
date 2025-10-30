# api/routes_recommendation.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from server.src.db.base import get_db
from server.src.middlewares.auth_middleware import get_current_user_from_db
from server.src.models.user_model import User
from server.src.services.recommendation_service import get_recommendations_for_user
from server.src.services.weather_service import WeatherService
from server.src.core.config import (
    WEATHER_API_KEY
)
import os

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

def get_weather_service() -> WeatherService:
    return WeatherService(api_key=WEATHER_API_KEY or "")

@router.get("/")
def recommendations(
    city: str = Query(None, description="Ville pour filtrer selon la météo"),
    is_outdoor: bool = Query(None, description="Filtrer les activités selon indoor/outdoor"),
    current_user: User = Depends(get_current_user_from_db),
    db: Session = Depends(get_db)
):
    """
    Retourne les recommandations pour l'utilisateur connecté.
    Optionnellement filtrées selon la météo si city est fournie.
    """
    return get_recommendations_for_user(current_user, db, city=city, is_outdoor=is_outdoor, weather_service=get_weather_service())
