from typing import AsyncGenerator

from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def get_session() -> AsyncGenerator:
    engine = create_async_engine(settings.DB_URL)

    session: AsyncSession = AsyncSession(engine)

    try:
        yield session
    finally:
        await session.close()
