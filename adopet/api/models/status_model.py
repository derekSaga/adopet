from api.enums.status_enum import StatusEnum
from api.models.base_model import StandardModelMixin
from core.config import settings
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column

BASE = declarative_base(cls=StandardModelMixin)


class StatusModel(BASE):
    name: Mapped[str] = mapped_column(
        Enum(
            StatusEnum,
            values_callable=lambda obj: [e.value for e in obj],
            create_constraint=True,
            schema=settings.DATABASE_SCHEMA,
        ),
        nullable=False,
    )
