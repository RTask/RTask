"""add statusid to column

Revision ID: 1e5e80482bc7
Revises: 5783db9372ff
Create Date: 2019-11-15 05:46:01.334816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e5e80482bc7'
down_revision = '5783db9372ff'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ticket', sa.Column('statusId', sa.BigInteger, sa.ForeignKey('status.id')))


def downgrade():
    op.drop_column('ticket', 'statusId')
