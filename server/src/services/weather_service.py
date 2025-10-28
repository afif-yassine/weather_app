import requests
from typing import Any, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY manquant : mets ta clé dans .env")
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def _make_api_call(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Méthode générique pour appeler l'API OpenWeatherMap"""
        url = f"{self.base_url}{endpoint}"
        
        # Paramètres par défaut
        default_params = {
            "appid": self.api_key,
            "units": "metric",
            "lang": "fr"
        }
        default_params.update(params)
        
        try:
            logger.info(f"Appel API OpenWeather: {endpoint} avec params: {params}")
            response = requests.get(url, params=default_params, timeout=15.0)
            response.raise_for_status()  # Lève une exception pour les codes 4xx/5xx
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erreur HTTP {response.status_code}: {e}")
            raise
        except requests.exceptions.Timeout:
            logger.error("Timeout lors de l'appel à l'API OpenWeather")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Erreur de connexion à l'API OpenWeather")
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue: {e}")
            raise

    def get_current_weather(self, city: str) -> Dict[str, Any]:
        """Récupère la météo actuelle avec gestion d'erreur améliorée"""
        params = {"q": city}
        return self._make_api_call("/weather", params)

    def get_forecast_raw(self, city: str) -> Dict[str, Any]:
        """Récupère les prévisions sur 5 jours (3h par 3h)"""
        params = {"q": city}
        return self._make_api_call("/forecast", params)
    
    def get_weather_by_coords(self, lat: float, lon: float) -> Dict[str, Any]:
        """Récupère la météo par coordonnées GPS"""
        params = {"lat": lat, "lon": lon}
        return self._make_api_call("/weather", params)
    
    def get_forecast_by_coords(self, lat: float, lon: float) -> Dict[str, Any]:
        """Récupère les prévisions par coordonnées GPS"""
        params = {"lat": lat, "lon": lon}
        return self._make_api_call("/forecast", params)