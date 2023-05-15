import random
from typing import Any
from typing import Dict

from api.enums.user_role_enum import UserRoleEnum
from api.models.repositories.user_repository import UserRepository
from faker import Faker
from fastapi.testclient import TestClient

myFactory = Faker(locale="pt_BR")


def user_data_with_password() -> Dict[str, Any]:
    return {
        "name": myFactory.name(),
        "email": myFactory.email(),
        "phone_number": myFactory.msisdn(),
        "password": user_password(),
        "role": random.choice(list(UserRoleEnum)).value,
        "about": myFactory.text(),
        "photo_url": myFactory.image_url(),
    }


def user_password() -> str:
    return "test_password"


def user_authentication_headers(client: TestClient, email: str, password: str) -> str:
    data = {"username": email, "password": password}
    r = client.post("/user/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return auth_token


async def authentication_token_from_email(
    client: TestClient, email: str, user_repository: UserRepository
) -> str:
    password = user_password()
    user = await user_repository.get_user_by_email(email=email)
    return user_authentication_headers(
        client=client, email=user.email, password=password
    )
