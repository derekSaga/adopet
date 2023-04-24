from datetime import datetime
from typing import Generator

from api.models.user_model import UserModel
from api.schemas.v1.token_schema import SystemUser
from api.schemas.v1.token_schema import TokenPayload
from core.config import settings
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

reusable_oauth = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login")


async def get_session() -> Generator:
    engine = create_async_engine(settings.DB_URL)

    session: AsyncSession = AsyncSession(engine)

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
    token: str = Depends(reusable_oauth), db: AsyncSession = Depends(get_session)
) -> SystemUser:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    query = select(UserModel).where(UserModel.email == token_data.sub)
    result = await db.execute(query)
    user = result.scalars().unique().one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(id=user.id, email=user.email, password=user.password)
