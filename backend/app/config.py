from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/risklens"
    MODEL_PATH: str = "trained_models"
    FRAUD_THRESHOLD: float = 0.7
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
