from uuid import UUID

from api.models.base_model import StandardModelMixin
from api.models.state_model import StateModel
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

BASE = declarative_base(cls=StandardModelMixin)


class CityModel(BASE):
    name: Mapped[str] = mapped_column(String, nullable=False)
    state_id: Mapped[UUID] = mapped_column(
        ForeignKey(StateModel.id, ondelete="CASCADE"), nullable=False
    )
    state: Mapped["StateModel"] = relationship(
        back_populates="cities",
    )
