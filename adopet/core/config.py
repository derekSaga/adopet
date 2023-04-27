import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
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

    ACCESS_TOKEN_EXPIRE_MINUTES = 1  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 1 * 7  # 7 days
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "my_super_secret"
    JWT_REFRESH_SECRET_KEY = (
        os.getenv("JWT_REFRESH_SECRET_KEY") or "my_refresh_super_secret"
    )

    class Config:
        case_sensitive = True


settings: Settings = Settings()
