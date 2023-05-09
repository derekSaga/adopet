import pytest
from api.models.repositories.user_repository import UserRepository
from api.models.user_model import UserModel
from api.schemas.v1.user_schema import UserSchemaCreate
from api.views.v1.utils.auth import get_hashed_password
from core.config import Settings
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from tests.support.utils import user_password

myFactory = Faker(locale="pt_BR")


@pytest.fixture(autouse=True)
async def test_user(
    fxt_async_session: AsyncSession, fxt_settings: Settings
) -> UserSchemaCreate:
    new_user = UserModel(
        name=myFactory.name(),
        email=myFactory.email(),
        phone_number=myFactory.phone_number(),
        password=user_password(),
        role="myFactory.role()",
        about=myFactory.text(),
        photo_url=myFactory.domain_name(),
    )

    new_user.metadata.schema = fxt_settings.DATABASE_SCHEMA

    new_user.password = get_hashed_password(new_user.password)

    user_repo = UserRepository(fxt_async_session)

    existing_user = await user_repo.get_user_by_email(email=new_user.email)

    new_user.photo_url = "da.com"

    unique_url_photo = await user_repo.check_value_is_unique(
        "photo_url", new_user.photo_url
    )

    while unique_url_photo is not None:
        new_user.photo_url = myFactory.domain_name()

        unique_url_photo = await user_repo.check_value_is_unique(
            "photo_url", new_user.photo_url
        )
    if existing_user is None:
        existing_user = await user_repo.create_user(new_user)

    yield existing_user

    await user_repo.delete_user_by_email(email=new_user.email)
