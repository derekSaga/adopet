"""user model

Revision ID: fe94ee4c8f66
Revises: 993e09fc1bff
Create Date: 2023-04-21 22:11:30.350473

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fe94ee4c8f66'
down_revision = '993e09fc1bff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('name', sa.String(length=155), nullable=False),
                    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
                    sa.Column('phone_number', sa.String(), nullable=False),
                    sa.Column('password', sqlalchemy_utils.types.password.PasswordType(max_length=8), nullable=True),
                    sa.Column('role', sa.String(), nullable=False),
                    sa.Column('about', sa.String(), nullable=False),
                    sa.Column('phot_url', sqlalchemy_utils.types.url.URLType(), nullable=True),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
