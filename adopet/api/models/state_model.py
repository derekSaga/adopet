from typing import List

from api.enums.state_enum import StateEnum
from api.models.base_model import StandardModelMixin
from core.config import settings
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

BASE = declarative_base(cls=StandardModelMixin)


class StateModel(BASE):
    name: Mapped[str] = mapped_column(
        Enum(
            StateEnum,
            values_callable=lambda obj: [e.value for e in obj],
            create_constraint=True,
            schema=settings.DATABASE_SCHEMA,
        ),
        nullable=False,
    )

    cities: Mapped[List["CityModel"]] = relationship(
        back_populates="state",
    )
