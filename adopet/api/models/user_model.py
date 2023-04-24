from api.models.base_model import StandardModelMixin
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import URLType

BASE = declarative_base(cls=StandardModelMixin)


class UserModel(BASE):
    __tablename__ = "user"
    name = Column(types.String(155), nullable=False)
    email = Column(EmailType, nullable=False, index=True, unique=True)
    phone_number = Column(types.String, nullable=False)
    password = Column(
        types.String,
        unique=True,
    )
    role = Column(types.String, nullable=False)
    about = Column(types.String, nullable=False)
    photo_url = Column(URLType, nullable=True)
