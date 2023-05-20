from typing import Any
from typing import Generator

import pytest
from api.models.repositories.user_repository import UserRepository
from api.models.user_model import UserModel
from api.views.v1.api import api_router
from core.config import Settings
from core.config import settings
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from tests.support.utils import authentication_token_from_email


@pytest.fixture
def fxt_settings() -> Settings:
    return Settings()


def start_application():
    app = FastAPI()
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app


@pytest.fixture(autouse=True)
async def fxt_async_engine(fxt_settings: Settings) -> AsyncEngine:
    engine = create_async_engine(fxt_settings.DB_URL, echo=False)
    async with engine.connect() as conn:
        await conn.execute(
            text("CREATE SCHEMA IF NOT EXISTS %s" % fxt_settings.DATABASE_SCHEMA)
        )

        UserModel.metadata.schema = fxt_settings.DATABASE_SCHEMA
        await conn.run_sync(UserModel.metadata.create_all)

        await conn.commit()

        yield engine

        await conn.execute(
            text("DROP SCHEMA %s CASCADE" % fxt_settings.DATABASE_SCHEMA)
        )

        await conn.commit()


@pytest.fixture(autouse=True)
async def fxt_async_session(fxt_async_engine: AsyncEngine) -> AsyncSession:
    session: AsyncSession = AsyncSession(fxt_async_engine)

    try:
        yield session
    finally:
        await session.close()


@pytest.fixture
def app(fxt_async_session: AsyncSession) -> Generator[FastAPI, Any, None]:
    _app = start_application()

    yield _app


@pytest.fixture
def client(
    app: FastAPI, fxt_async_session: AsyncSession
) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
async def client_test(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app, base_url="http://test", follow_redirects=True
    ) as ac:
        ac.headers["Content-Type"] = "application/json"
        yield ac


@pytest.fixture
async def normal_user_token_headers(
    client: TestClient, fxt_async_session: AsyncSession, test_user: UserModel
):
    user_repository = UserRepository(fxt_async_session)

    yield await authentication_token_from_email(
        client=client, email=test_user.email, user_repository=user_repository
    )
