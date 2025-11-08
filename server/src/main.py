from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi

# Import des routers
from server.src.api.routes_weather import router as weather_router
from server.src.api.routes_recommendation import router as routes_recommendation
from server.src.api.routes_address import router as routes_address
from server.src.api.routes_auth import router as auth_router
from server.src.api.routes_activity import router as activity_router
from server.src.api.routes_category import router as category_router
from server.src.api.routes_history import router as routes_history
from server.src.api.routes_tag import router as tag_router
from server.src.api.routes_preference import router as preference_router

# Import des middlewares
from server.src.middlewares.auth_middleware import jwt_middleware, get_current_user

# Import des modèles et base
from server.src.db.base import Base, engine, SessionLocal
from server.src.models.user_model import Base as UserBase
from server.src.models.role_model import Base as RoleBase
from server.src.core.init_roles import init_roles, init_admin

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Initialisation des rôles et admin par défaut
db = SessionLocal()
init_roles(db)
init_admin(db, email="admin@example.com", username="admin", password="Admin123!")
db.close()

# -----------------------------
# 🚀 App FastAPI
# -----------------------------
app = FastAPI(
    title="Weather API", version="1.0", description="API météo 🌦️ avec JWT et rôles"
)

# -----------------------------
# Middleware JWT global (optionnel)
# -----------------------------
# app.middleware("http")(jwt_middleware)

# -----------------------------
# Routes
# -----------------------------
app.include_router(auth_router)
app.include_router(routes_address)
app.include_router(weather_router)
app.include_router(activity_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(preference_router)
app.include_router(routes_recommendation)
app.include_router(routes_history)


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API météo 🌦️ avec Auth 🔐"}


# -----------------------------
# Swagger : ajout du Bearer token
# -----------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Weather API",
        version="1.0",
        description="API météo 🌦️ avec JWT et rôles",
        routes=app.routes,
    )

    # Définir le schéma de sécurité global
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    # Appliquer BearerAuth sur toutes les routes sauf /auth/*
    for path, path_item in openapi_schema["paths"].items():
        if not path.startswith("/auth"):
            for method in path_item.values():
                method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
