"""state model

Revision ID: 5c5afc62f994
Revises:
Create Date: 2023-04-26 20:02:48.002842

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5c5afc62f994"
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
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="adopet",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("state", schema="adopet")
    op.execute("DROP SCHEMA IF EXISTS adopet RESTRICT")
    # ### end Alembic commands ###
