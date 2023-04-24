"""state and city model

Revision ID: 82d08229a244
Revises: 
Create Date: 2023-04-24 01:05:26.453106

"""
import sqlalchemy as sa
from alembic import op
from api.enums.state_enum import StateEnum
from api.models.state_model import StateModel

# revision identifiers, used by Alembic.
revision = "82d08229a244"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS adopet")
    op.create_table(
        "state",
        sa.Column(
            "name",
            sa.Enum(
                "Rondônia",
                "Acre",
                "Amazonas",
                "Roraima",
                "Pará",
                "Amapá",
                "Tocantins",
                "Maranhão",
                "Piauí",
                "Ceará",
                "Rio Grande do Norte",
                "Paraíba",
                "Pernambuco",
                "Alagoas",
                "Sergipe",
                "Bahia",
                "Minas Gerais",
                "Espírito Santo",
                "Rio de Janeiro",
                "São Paulo",
                "Paraná",
                "Santa Catarina",
                "Rio Grande do Sul",
                "Mato Grosso do Sul",
                "Mato Grosso",
                "Goiás",
                "Distrito Federal",
                name="stateenum",
                schema="adopet",
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="adopet",
    )
    op.create_table(
        "city",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("state_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["state_id"],
            ["adopet.state.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="adopet",
    )
    # ### end Alembic commands ###
    op.bulk_insert(StateModel.__table__, [{"name": value.value} for value in StateEnum])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("city", schema="adopet")
    op.drop_table("state", schema="adopet")
    op.execute("DROP SCHEMA IF EXISTS adopet RESTRICT")
    # ### end Alembic commands ###