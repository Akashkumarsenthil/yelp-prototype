from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/yelp_db"
    SECRET_KEY: str = "change-me-to-a-real-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENAI_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
