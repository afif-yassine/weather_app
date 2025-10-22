import os
from dotenv import load_dotenv

load_dotenv()

# database settings
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# weather api
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# JWT settings
SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
ALGORITHM = os.getenv("ALGORITHM")


# Fonction utilitaire pour parser les durées du .env (1h, 7d, etc.)
def parse_duration(value: str) -> int:
    if value.endswith("h"):
        return int(value[:-1]) * 60          # convertit heures → minutes
    elif value.endswith("d"):
        return int(value[:-1]) * 24 * 60     # convertit jours → minutes
    else:
        return int(value)                    # minutes par défaut

ACCESS_TOKEN_EXPIRE_MINUTES = parse_duration(os.getenv("ACCESS_TOKEN_EXPIRE", "15"))
REFRESH_TOKEN_EXPIRE_MINUTES = parse_duration(os.getenv("REFRESH_TOKEN_EXPIRE", "10080"))