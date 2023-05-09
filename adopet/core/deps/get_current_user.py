from datetime import datetime

from api.models.user_model import UserModel
from api.schemas.v1.token_schema import SystemUser
from api.schemas.v1.token_schema import TokenPayload
from core.config import settings
from core.deps.get_session_db import get_session
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

reusable_oauth = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/user/login")


async def get_current_user_request(
    token: str = Depends(reusable_oauth), db: AsyncSession = Depends(get_session)
) -> SystemUser:
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp).utcnow() < datetime.utcnow():
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
