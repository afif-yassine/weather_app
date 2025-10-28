from typing import Any, Dict, List
from collections import defaultdict
from datetime import datetime
import logging
from server.src.schemas.weather_schema import CurrentWeatherOut, ForecastOut, ForecastDay

logger = logging.getLogger(__name__)

def map_current_weather(city: str, data: Dict[str, Any]) -> CurrentWeatherOut:
    """
    Transforme la réponse OpenWeatherMap en CurrentWeatherOut amélioré
    """
    try:
        # Extraction des données
        weather_info = (data.get("weather") or [{}])[0]
        main_data = data.get("main") or {}
        wind_data = data.get("wind") or {}
        sys_data = data.get("sys") or {}
        coord_data = data.get("coord") or {}
        
        # Conversion des timestamps
        sunrise = datetime.fromtimestamp(sys_data.get('sunrise', 0))
        sunset = datetime.fromtimestamp(sys_data.get('sunset', 0))
        
        return CurrentWeatherOut(
            # Informations de base
            city=data.get("name", city),
            country=sys_data.get("country", "Unknown"),
            
            # Conditions
            condition=weather_info.get("main", "Clear"),
            description=weather_info.get("description", ""),
            icon=weather_info.get("icon", ""),
            
            # Températures
            temp_c=main_data.get("temp", 0),
            feels_like_c=main_data.get("feels_like", 0),
            temp_min=main_data.get("temp_min", 0),
            temp_max=main_data.get("temp_max", 0),
            
            # Autres mesures
            humidity=main_data.get("humidity", 0),
            pressure=main_data.get("pressure", 0),
            wind_speed=wind_data.get("speed", 0),
            wind_deg=wind_data.get("deg", 0),
            visibility=data.get("visibility", 0),
            cloudiness=data.get("clouds", {}).get("all", 0),
            
            # Temps
            sunrise=sunrise,
            sunset=sunset,
            
            # Coordonnées
            lat=coord_data.get("lat", 0),
            lon=coord_data.get("lon", 0),
            
            # Métadonnées
            last_updated=datetime.now(),
            mock=False
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du mapping de la météo pour {city}: {e}")
        # Fallback avec données minimales
        return CurrentWeatherOut(
            city=city,
            country="Unknown",
            condition="Unknown",
            description="Data unavailable",
            icon="",
            temp_c=0,
            feels_like_c=0,
            temp_min=0,
            temp_max=0,
            humidity=0,
            pressure=0,
            wind_speed=0,
            wind_deg=0,
            visibility=0,
            cloudiness=0,
            sunrise=datetime.now(),
            sunset=datetime.now(),
            lat=0,
            lon=0,
            last_updated=datetime.now(),
            mock=False
        )

def map_forecast(city: str, days: int, data: Dict[str, Any]) -> ForecastOut:
    """
    Transforme les données de prévision OpenWeatherMap en ForecastOut amélioré
    """
    try:
        city_data = data.get("city", {})
        forecast_list = data.get("list", [])
        
        # Groupement des prévisions par jour
        daily_forecasts = _group_forecast_by_day(forecast_list)
        
        # Création des ForecastDay pour le nombre de jours demandé
        forecast_days = _create_detailed_forecast_days(daily_forecasts, days)
        
        return ForecastOut(
            city=city_data.get("name", city),
            country=city_data.get("country", "Unknown"),
            days=days,
            lat=city_data.get("coord", {}).get("lat", 0),
            lon=city_data.get("coord", {}).get("lon", 0),
            forecast=forecast_days,
            generated_at=datetime.now(),
            mock=False
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du mapping des prévisions pour {city}: {e}")
        # Retourne une prévision vide en cas d'erreur
        return ForecastOut(
            city=city,
            country="Unknown",
            days=days,
            lat=0,
            lon=0,
            forecast=[],
            generated_at=datetime.now(),
            mock=False
        )

def _group_forecast_by_day(forecast_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Groupe les prévisions par jour"""
    daily_data = defaultdict(list)
    
    for item in forecast_list:
        dt_txt = item.get("dt_txt", "")
        if not dt_txt:
            continue
            
        # Extraction de la date (YYYY-MM-DD)
        date_str = dt_txt.split(" ")[0]
        
        # Validation de la date
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            daily_data[date_str].append(item)
        except ValueError:
            continue
    
    return dict(daily_data)

def _create_detailed_forecast_days(daily_forecasts: Dict[str, List[Dict[str, Any]]], max_days: int) -> List[ForecastDay]:
    """Crée les objets ForecastDay détaillés"""
    forecast_days = []
    
    # Trie les dates et prend les X premiers jours
    sorted_dates = sorted(daily_forecasts.keys())[:max_days]
    
    for date in sorted_dates:
        day_forecasts = daily_forecasts[date]
        
        if not day_forecasts:
            continue
            
        # Agrégation des données pour la journée
        day_summary = _aggregate_daily_data(day_forecasts)
        
        forecast_days.append(ForecastDay(
            date=date,
            condition=day_summary["condition"],
            description=day_summary["description"],
            icon=day_summary["icon"],
            temp_avg=day_summary["temp_avg"],
            temp_min=day_summary["temp_min"],
            temp_max=day_summary["temp_max"],
            feels_like_avg=day_summary["feels_like_avg"],
            humidity=day_summary["humidity"],
            pressure=day_summary["pressure"],
            wind_speed=day_summary["wind_speed"],
            pop=day_summary["pop"],
            sunrise=day_summary["sunrise"],
            sunset=day_summary["sunset"]
        ))
    
    return forecast_days

def _aggregate_daily_data(day_forecasts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Agrège les données pour une journée complète"""
    # Initialisation des listes de données
    temps = []
    feels_like = []
    humidities = []
    pressures = []
    wind_speeds = []
    pops = []
    conditions = []
    descriptions = []
    icons = []
    
    # Lever/coucher de soleil (premier élément de la journée)
    first_item = day_forecasts[0]
    sunrise = datetime.fromtimestamp(first_item.get('sys', {}).get('sunrise', 0))
    sunset = datetime.fromtimestamp(first_item.get('sys', {}).get('sunset', 0))
    
    for forecast in day_forecasts:
        main_data = forecast.get("main") or {}
        weather_data = (forecast.get("weather") or [{}])[0]
        wind_data = forecast.get("wind") or {}
        
        # Collecte des données numériques
        temps.append(main_data.get("temp", 0))
        feels_like.append(main_data.get("feels_like", 0))
        humidities.append(main_data.get("humidity", 0))
        pressures.append(main_data.get("pressure", 0))
        wind_speeds.append(wind_data.get("speed", 0))
        pops.append(forecast.get("pop", 0))  # Probability of Precipitation
        
        # Conditions météo
        conditions.append(weather_data.get("main", "Clear"))
        descriptions.append(weather_data.get("description", ""))
        icons.append(weather_data.get("icon", ""))
    
    # Calcul des moyennes et extrêmes
    def safe_avg(values):
        return round(sum(values) / len(values), 1) if values else 0
    
    def safe_mode(values):
        return max(set(values), key=values.count) if values else "Clear"
    
    return {
        "condition": safe_mode(conditions),
        "description": safe_mode(descriptions),
        "icon": safe_mode(icons),
        "temp_avg": safe_avg(temps),
        "temp_min": min(temps) if temps else 0,
        "temp_max": max(temps) if temps else 0,
        "feels_like_avg": safe_avg(feels_like),
        "humidity": round(safe_avg(humidities)),
        "pressure": round(safe_avg(pressures)),
        "wind_speed": safe_avg(wind_speeds),
        "pop": round(safe_avg(pops), 2),
        "sunrise": sunrise,
        "sunset": sunset
    }