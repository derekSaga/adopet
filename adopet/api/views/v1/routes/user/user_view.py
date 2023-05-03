import logging

from api.models.user_model import UserModel
from api.schemas.v1.token_schema import SystemUser
from api.schemas.v1.token_schema import TokenSchema
from api.schemas.v1.token_schema import UserOut
from api.schemas.v1.user_schema import UserSchemaBase
from api.schemas.v1.user_schema import UserSchemaCreate
from api.views.v1.utils.auth import create_access_token
from api.views.v1.utils.auth import create_refresh_token
from api.views.v1.utils.auth import get_hashed_password
from api.views.v1.utils.auth import verify_password
from core.deps.get_current_user import get_current_user_request
from core.deps.get_session_db import get_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaBase,
    summary="Create new user",
)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    logger.info("creating user".title())
    new_user: UserModel = UserModel(**user.dict())

    new_user.password = get_hashed_password(new_user.password)
    try:
        async with db as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    except Exception as error:
        logger.error(error, exc_info=True)
        raise error


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    query = select(UserModel).where(UserModel.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().unique().one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def get_me(user: SystemUser = Depends(get_current_user_request)):
    return user
