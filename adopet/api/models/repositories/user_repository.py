import logging
from typing import Union

from api.models.repositories.base_repository import BaseRepository
from api.models.user_model import UserModel
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_user(self, new_user: UserModel) -> UserModel:
        try:
            async with self.session as session:
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                return new_user

        except Exception as error:
            logger.error(error, exc_info=True)
            raise error

    async def get_user_by_email(
        self, email: Union[EmailStr, str]
    ) -> Union[UserModel, None]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user = result.scalars().unique().one_or_none()
        return user

    async def delete_user_by_email(self, email: Union[EmailStr, str]) -> None:
        deleted_objects = UserModel.__table__.delete().where(UserModel.email == email)
        await self.session.execute(deleted_objects)
        await self.session.commit()

    async def check_value_is_unique(self, field_name: str, value_field: str):
        query = select(UserModel).filter(getattr(UserModel, field_name) == value_field)
        result = await self.session.execute(query)
        value = result.scalar()
        return value

    async def get_user_by_unique_constraint(
        self, user_search: UserModel
    ) -> Union[UserModel, None]:
        query = select(UserModel)

        filters = self.get_filter_by_constraints_from_table_model(
            UserModel, user_search
        )
        query_execute = await self.session.execute(query.filter(*filters))

        result = query_execute.scalars().unique().one_or_none()

        return result

    async def get_all_users(self, role: str, **kwargs):
        query = select(UserModel).filter(text(f"{UserModel.role.name} = '{role}'"))
        result = await paginate(self.session, query, **kwargs)
        return result
