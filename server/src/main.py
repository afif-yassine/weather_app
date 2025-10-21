from fastapi import FastAPI
from server.src.api.routes_weather import router as weather_router
from server.src.db.base import Base, engine
from server.src.models.weather_model import Base

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather API",
    version="1.0",
    description="API de gestion des données météo 🌦️"
)

# Routes
app.include_router(weather_router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API météo 👋"}
