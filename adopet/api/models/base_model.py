from datetime import datetime
from uuid import UUID
from uuid import uuid4

from core.config import settings
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class StandardModelMixin(object):
    __table_args__ = {"schema": settings.DATABASE_SCHEMA}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.replace("Model", "").lower()

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )
