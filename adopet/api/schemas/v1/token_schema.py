from typing import Union
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import StrictStr


class TokenSchema(BaseModel):
    access_token: StrictStr
    refresh_token: StrictStr


class TokenPayload(BaseModel):
    sub: Union[str, None] = None
    exp: Union[float, int, None] = None


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    password: StrictStr = Field(
        ..., min_length=5, max_length=24, description="user password"
    )


class UserOut(BaseModel):
    id: UUID
    email: EmailStr


class SystemUser(UserOut):
    password: str
