"""add read to message table

Revision ID: 5d8d9eba3f80
Revises: 0a2392f05810
Create Date: 2019-11-15 04:57:35.125051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d8d9eba3f80'
down_revision = '0a2392f05810'
branch_labels = None
depends_on = None


def upgrade():
   op.add_column('messages', sa.Column('read', sa.Boolean))


def downgrade():
    op.drop_column('messages', 'read')
