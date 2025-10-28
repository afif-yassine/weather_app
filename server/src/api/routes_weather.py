from fastapi import APIRouter, HTTPException, Query, Depends
import requests
import logging
from server.src.core.config import (
    WEATHER_API_KEY
)
from server.src.schemas.weather_schema import CurrentWeatherOut, ForecastOut
from server.src.services.weather_service import WeatherService
from server.src.services.weather_adapter import map_current_weather, map_forecast

router = APIRouter(prefix="/weather", tags=["Meteo"])
logger = logging.getLogger(__name__)

# Dépendance pour le service météo
def get_weather_service() -> WeatherService:
    return WeatherService(api_key=WEATHER_API_KEY or "")

@router.get("/{city}", response_model=CurrentWeatherOut, summary="Météo actuelle")
def current_weather(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):
    """
    Récupère la météo actuelle pour une ville spécifique.
    
    - **city**: Nom de la ville (ex: Paris, London, New York)
    """
    if not city or not city.strip():
        raise HTTPException(
            status_code=400, 
            detail="Le nom de la ville est requis"
        )
    
    try:
        logger.info(f"Requête météo actuelle pour: {city}")
        data = service.get_current_weather(city.strip())
        return map_current_weather(city, data)
        
    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        error_detail = _handle_http_error(status_code, city)
        logger.warning(f"Erreur HTTP {status_code} pour {city}: {error_detail}")
        raise HTTPException(status_code=status_code, detail=error_detail)
        
    except Exception as e:
        logger.error(f"Erreur inattendue pour {city}: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne du serveur"
        )

@router.get("/{city}/forecast", response_model=ForecastOut, summary="Prévisions météo")
def forecast(
    city: str,
    days: int = Query(3, ge=1, le=7, description="Nombre de jours de prévision (1-7)"),
    service: WeatherService = Depends(get_weather_service)
):
    """
    Récupère les prévisions météo pour une ville sur plusieurs jours.
    
    - **city**: Nom de la ville
    - **days**: Nombre de jours de prévision (1-7, défaut: 3)
    """
    if not city or not city.strip():
        raise HTTPException(
            status_code=400, 
            detail="Le nom de la ville est requis"
        )
    
    try:
        logger.info(f"Requête prévisions pour: {city}, {days} jours")
        data = service.get_forecast_raw(city.strip())
        return map_forecast(city, days, data)
        
    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        error_detail = _handle_http_error(status_code, city)
        logger.warning(f"Erreur HTTP {status_code} pour prévisions {city}: {error_detail}")
        raise HTTPException(status_code=status_code, detail=error_detail)
        
    except Exception as e:
        logger.error(f"Erreur inattendue pour prévisions {city}: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne du serveur"
        )

def _handle_http_error(status_code: int, city: str) -> str:
    """Gère les erreurs HTTP spécifiques à l'API OpenWeatherMap"""
    error_messages = {
        400: "Requête invalide",
        401: "Clé API invalide",
        404: f"Ville '{city}' non trouvée",
        429: "Limite de requêtes dépassée",
        500: "Erreur du service météo",
        502: "Service météo temporairement indisponible",
        503: "Service météo en maintenance",
        504: "Timeout du service météo"
    }
    
    return error_messages.get(status_code, f"Erreur {status_code}")

# Route de santé pour vérifier que l'API fonctionne
@router.get("/health/check")
def health_check(service: WeatherService = Depends(get_weather_service)):
    """Vérifie la santé de l'API météo"""
    try:
        # Test avec une ville simple
        test_city = "London"
        data = service.get_current_weather(test_city)
        
        return {
            "status": "healthy",
            "service": "openweathermap",
            "test_city": test_city,
            "api_key_configured": bool(WEATHER_API_KEY)
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service météo indisponible"
        )