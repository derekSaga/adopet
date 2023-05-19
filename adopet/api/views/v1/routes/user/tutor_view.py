import logging

from api.enums.user_role_enum import UserRoleEnum
from api.models.repositories.user_repository import UserRepository
from api.models.user_model import UserModel
from api.schemas.v1.user_schema import UserList
from api.schemas.v1.user_schema import UserSchemaBase
from api.schemas.v1.user_schema import UserSchemaCreate
from api.views.v1.utils.auth import get_hashed_password
from core.deps.get_session_db import get_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi_pagination import Page
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaBase,
    summary="Create new tutor",
)
async def post_tutor(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    logger.info("creating user".title())

    user_data = user.dict()

    user_data.update({"role": UserRoleEnum.TUTOR.value})

    new_user: UserModel = UserModel(**user_data)

    new_user.password = get_hashed_password(new_user.password)
    try:
        result = await UserRepository(db).create_user(new_user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.orig.__cause__.detail).title(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@router.get(path="/", summary="List all tutors", response_model=Page[UserList])
async def get_tutors(db: AsyncSession = Depends(get_session)):
    users = await UserRepository(db).get_all_users(UserRoleEnum.TUTOR.value)
    return users
