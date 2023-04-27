"""city model

Revision ID: 8580260f9df2
Revises: 85085d68e2e1
Create Date: 2023-04-26 20:07:52.017734

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8580260f9df2"
down_revision = "85085d68e2e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS adopet")
    op.create_table(
        "city",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("state_id", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["state_id"], ["adopet.state.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        schema="adopet",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("city", schema="adopet")
    op.execute("DROP SCHEMA IF EXISTS adopet RESTRICT")
    # ### end Alembic commands ###