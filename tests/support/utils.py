from api.models.repositories.user_repository import UserRepository
from fastapi.testclient import TestClient


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
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = user_password()
    user = await user_repository.get_user_by_email(email=email)
    return user_authentication_headers(
        client=client, email=user.email, password=password
    )
