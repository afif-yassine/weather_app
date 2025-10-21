from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from server.src.core.config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT,
)

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base commune pour tous les modèles
Base = declarative_base()

# Test rapide
if __name__ == "__main__":
    with engine.connect() as conn:
        result = conn.execute("SELECT 'Connexion OK!'")
        print(result.scalar())
