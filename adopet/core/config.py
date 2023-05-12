import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = os.environ["API_V1_STR"]
    API_PORT: int = int(os.environ["API_PORT"])

    DB_URL: str = "%s://%s:%s@%s:%s/%s" % (
        os.environ["DRIVER_NAME"],
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["DATABASE_HOST"],
        os.environ["DATABASE_PORT"],
        os.environ["POSTGRES_DB"],
    )
    DATABASE_SCHEMA: str = os.environ["DATABASE_SCHEMA"]

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"])
    ALGORITHM: str = os.environ["ALGORITHM"]
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
    JWT_REFRESH_SECRET_KEY: str = os.environ["JWT_REFRESH_SECRET_KEY"]

    class Config:
        case_sensitive = True


settings: Settings = Settings()
