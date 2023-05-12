from api.models.base_model import StandardModelMixin
from sqlalchemy import types
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import URLType

BASE = declarative_base(cls=StandardModelMixin)


class UserModel(BASE):
    name: Mapped[str] = mapped_column(types.String(155), nullable=False)
    email: Mapped[str] = mapped_column(
        EmailType, nullable=False, index=True, unique=True
    )
    phone_number: Mapped[str] = mapped_column(types.String, nullable=False, unique=True)
    password: Mapped[str]
    role: Mapped[str]
    about: Mapped[str]
    photo_url: Mapped[str] = mapped_column(URLType, nullable=False, unique=True)
