from api.enums.state_enum import StateEnum
from api.models.base_model import StandardModelMixin
from core.config import settings
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

BASE = declarative_base(cls=StandardModelMixin)


class StateModel(BASE):
    __tablename__ = "state"

    name = Column(
        Enum(
            StateEnum,
            values_callable=lambda obj: [e.value for e in obj],
            create_constraint=True,
            schema=settings.DATABASE_SCHEMA,
        ),
        nullable=False,
    )

    cities = relationship(
        "CityModel",
        back_populates="state",
        cascade="all, delete-orphan",
    )
