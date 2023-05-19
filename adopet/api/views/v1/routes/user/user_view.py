import logging

from api.models.repositories.user_repository import UserRepository
from api.schemas.v1.token_schema import SystemUser
from api.schemas.v1.token_schema import TokenSchema
from api.schemas.v1.token_schema import UserOut
from api.views.v1.utils.auth import create_access_token
from api.views.v1.utils.auth import create_refresh_token
from api.views.v1.utils.auth import verify_password
from core.deps.get_current_user import get_current_user_request
from core.deps.get_session_db import get_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await UserRepository(db).get_user_by_email(email=form_data.username)

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
