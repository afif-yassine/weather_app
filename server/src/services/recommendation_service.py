# server/src/services/recommendation_service.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from server.src.models.activity_model import Activity, Tag, Category
from server.src.models.user_model import User
from server.src.models.history_model import History
from server.src.services.weather_service import WeatherService
from server.src.schemas.weather_schema import CurrentWeatherOut
from datetime import datetime
import logging

logger = logging.getLogger("recommendation_service")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_recommendations_for_user(
    user: User, 
    db: Session, 
    city: str = None, 
    is_outdoor: bool = None,  
    weather_service: WeatherService = None, 
    limit: int = 5
):
    query = db.query(Activity).options(
        joinedload(Activity.categories),
        joinedload(Activity.tags)
    )

    # Filtrer selon l'âge
    if user.age is not None:
        query = query.filter(
            (Activity.min_age <= user.age) &
            ((Activity.max_age >= user.age) | (Activity.max_age.is_(None)))
        )

    # Historique
    user_history = db.query(History).filter(History.user_id == user.id).all()
    if user_history:
        viewed_ids = [h.activity_id for h in user_history]
        query = query.filter(~Activity.id.in_(viewed_ids))

    # Récupération brute
    activities = query.order_by(Activity.created_at.desc()).all()

    # Météo
    weather_data = None
    temp, condition = None, None
    if city and weather_service:
        try:
            raw_weather = weather_service.get_current_weather(city)
            temp = raw_weather.get("temp_c") or raw_weather.get("main", {}).get("temp")
            condition = raw_weather.get("condition") or raw_weather.get("weather", [{}])[0].get("main", "")

            weather_data = CurrentWeatherOut(
                city=raw_weather.get("name"),
                country=raw_weather.get("sys", {}).get("country"),
                condition=condition,
                description=raw_weather.get("weather", [{}])[0].get("description", ""),
                icon=raw_weather.get("weather", [{}])[0].get("icon", ""),
                temp_c=temp,
                feels_like_c=raw_weather.get("main", {}).get("feels_like"),
                temp_min=raw_weather.get("main", {}).get("temp_min"),
                temp_max=raw_weather.get("main", {}).get("temp_max"),
                humidity=raw_weather.get("main", {}).get("humidity"),
                pressure=raw_weather.get("main", {}).get("pressure"),
                wind_speed=raw_weather.get("wind", {}).get("speed"),
                wind_deg=raw_weather.get("wind", {}).get("deg"),
                visibility=raw_weather.get("visibility", 0),
                cloudiness=raw_weather.get("clouds", {}).get("all", 0),
                sunrise=datetime.fromtimestamp(raw_weather.get("sys", {}).get("sunrise", 0)),
                sunset=datetime.fromtimestamp(raw_weather.get("sys", {}).get("sunset", 0)),
                lat=raw_weather.get("coord", {}).get("lat"),
                lon=raw_weather.get("coord", {}).get("lon"),
                last_updated=datetime.utcnow(),
                mock=False
            )
        except Exception as e:
            logger.error(f"Impossible de récupérer la météo: {e}")

    # Filtrer les activités selon la météo (température + conditions)
    filtered_activities = []
    for act in activities:
        # Vérifier température
        if temp is not None:
            if act.ideal_temperature_min and temp < act.ideal_temperature_min:
                continue
            if act.ideal_temperature_max and temp > act.ideal_temperature_max:
                continue

        # Vérifier conditions météo
        if condition:
            if condition.lower() in ["rain", "snow"] and act.is_outdoor:
                continue

        
        # Vérifier is_outdoor passé en paramètre
        if is_outdoor is not None:
            if act.is_outdoor != is_outdoor:
                continue

        # Mettre à jour la météo pour l'activité
        act.weather_conditions = condition.lower() if condition else act.weather_conditions
        filtered_activities.append(act)

    # Limiter le nombre de recommandations
    recommendations = filtered_activities[:limit]

    return {
        "activities": recommendations,
        "weather": weather_data
    }
