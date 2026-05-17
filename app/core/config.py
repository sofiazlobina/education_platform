from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    APP_NAME: str = "Educational Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    AI_BASE_URL: str = "https://openrouter.ai/api/v1"
    AI_MODEL: str = "mistralai/mistral-small-3.1-24b-instruct:free"
    AI_API_KEY: str | None = None

    class Config:
        env_file = ".env"

# Эта функция нужна, чтобы настройки загружались только один раз
@lru_cache()
def get_settings() -> Settings:
    return Settings()