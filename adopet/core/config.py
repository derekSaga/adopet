import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    class Config:
        case_sensitive = True


settings: Settings = Settings()
