"""insert-enum-choices

Revision ID: bf687421e4d5
Revises: 80aeb6522db7
Create Date: 2023-04-26 20:12:40.508544

"""
from enum import Enum
from typing import Type

import alembic
from alembic import op
from api.enums.animal_species import AnimalSpecieEnum
from api.enums.size_enum import SizeEnum
from api.enums.state_enum import StateEnum
from api.enums.status_enum import StatusEnum
from api.models.animal_specie_model import AnimalSpecieModel
from api.models.size_model import SizeModel
from api.models.state_model import StateModel
from api.models.status_model import StatusModel
from sqlalchemy import Table

# revision identifiers, used by Alembic.
revision = "bf687421e4d5"
down_revision = "80aeb6522db7"
branch_labels = None
depends_on = None


def data_bulk_enum_insert(
    op_alembic: alembic, table: Type[Table], enum_class: Type[Enum]
):
    op_alembic.bulk_insert(
        table.__table__, [{"name": value.value} for value in enum_class]
    )


def upgrade() -> None:
    data_bulk_enum_insert(op, StateModel, StateEnum)
    data_bulk_enum_insert(op, SizeModel, SizeEnum)
    data_bulk_enum_insert(op, StatusModel, StatusEnum)
    data_bulk_enum_insert(op, AnimalSpecieModel, AnimalSpecieEnum)


def downgrade() -> None:
    pass
