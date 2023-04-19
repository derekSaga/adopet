import datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr

Base = declarative_base()


class StandardModelMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(types.UUID, name="id", primary_key=True, default=uuid4)
    created_at = Column(
        types.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    updated_at = Column(
        types.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
