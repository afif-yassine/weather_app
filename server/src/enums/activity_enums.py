# server/src/enums/activity_enums.py
import enum

class IntensityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class WeatherConditionEnum(str, enum.Enum):
    sunny = "sunny"
    rainy = "rainy"
    cloudy = "cloudy"
    snowy = "snowy"
    windy = "windy"
    foggy = "foggy"
    stormy = "stormy"

class LocationTypeEnum(str, enum.Enum):
    indoor = "indoor"
    outdoor = "outdoor"
    mixed = "mixed"

class AccessibilityLevelEnum(str, enum.Enum):
    easy = "easy"
    moderate = "moderate"
    hard = "hard"
