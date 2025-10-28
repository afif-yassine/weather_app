from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class CurrentWeatherOut(BaseModel):
    # Informations de base
    city: str = Field(..., description="Nom de la ville")
    country: str = Field(..., description="Code du pays")
    
    # Conditions météo principales
    condition: str = Field(..., description="Condition météo principale")
    description: str = Field(..., description="Description détaillée")
    icon: str = Field(..., description="Icône météo")
    
    # Températures
    temp_c: float = Field(..., description="Température actuelle en °C")
    feels_like_c: float = Field(..., description="Température ressentie en °C")
    temp_min: float = Field(..., description="Température minimale")
    temp_max: float = Field(..., description="Température maximale")
    
    # Autres mesures
    humidity: int = Field(..., description="Humidité en pourcentage")
    pressure: int = Field(..., description="Pression atmosphérique en hPa")
    wind_speed: float = Field(..., description="Vitesse du vent en m/s")
    wind_deg: int = Field(..., description="Direction du vent en degrés")
    visibility: int = Field(..., description="Visibilité en mètres")
    cloudiness: int = Field(..., description="Nébulosité en pourcentage")
    
    # Données temporelles
    sunrise: datetime = Field(..., description="Lever du soleil")
    sunset: datetime = Field(..., description="Coucher du soleil")
    
    # Coordonnées
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    
    # Métadonnées
    last_updated: datetime = Field(..., description="Dernière mise à jour des données")
    mock: bool = Field(False, description="Données simulées ou réelles")

class ForecastDay(BaseModel):
    date: str = Field(..., description="Date de la prévision (YYYY-MM-DD)")
    
    # Conditions
    condition: str = Field(..., description="Condition principale")
    description: str = Field(..., description="Description détaillée")
    icon: str = Field(..., description="Icône météo")
    
    # Températures
    temp_avg: float = Field(..., description="Température moyenne")
    temp_min: float = Field(..., description="Température minimale")
    temp_max: float = Field(..., description="Température maximale")
    feels_like_avg: float = Field(..., description="Température ressentie moyenne")
    
    # Autres données
    humidity: int = Field(..., description="Humidité moyenne")
    pressure: int = Field(..., description="Pression moyenne")
    wind_speed: float = Field(..., description="Vitesse moyenne du vent")
    pop: float = Field(..., description="Probability of Precipitation (0-1)")
    
    # Durée du jour
    sunrise: datetime = Field(..., description="Lever du soleil")
    sunset: datetime = Field(..., description="Coucher du soleil")

class ForecastOut(BaseModel):
    city: str = Field(..., description="Ville concernée")
    country: str = Field(..., description="Pays concerné")
    days: int = Field(..., description="Nombre de jours de prévision")
    
    # Localisation
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    
    # Prévisions
    forecast: List[ForecastDay] = Field(..., description="Prévisions quotidiennes")
    
    # Métadonnées
    generated_at: datetime = Field(..., description="Heure de génération du rapport")
    mock: bool = Field(False, description="Données simulées ou réelles")