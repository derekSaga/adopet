"""user role constraint

Revision ID: c97058b92c33
Revises: bf687421e4d5
Create Date: 2023-05-13 15:53:40.112494

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c97058b92c33"
down_revision = "bf687421e4d5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    banner_status = sa.Enum(
        "TUTOR",
        "ONG",
        "ASSOCIATION",
        name="userroleenum",
        schema="adopet",
        create_constraint=True,
    )
    banner_status.create(op.get_bind())

    op.execute("CREATE SCHEMA IF NOT EXISTS adopet")
    op.alter_column(
        "user",
        "role",
        existing_type=sa.VARCHAR(),
        type_=banner_status.enum_class,
        existing_nullable=False,
        schema="adopet",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "role",
        existing_type=sa.Enum(
            "TUTOR",
            "ONG",
            "ASSOCIATION",
            name="userroleenum",
            schema="adopet",
            create_constraint=True,
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        schema="adopet",
    )
    op.execute("DROP SCHEMA IF EXISTS adopet RESTRICT")
    # ### end Alembic commands ###
