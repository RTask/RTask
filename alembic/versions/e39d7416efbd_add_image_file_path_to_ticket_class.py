"""Add image file path to ticket class

Revision ID: e39d7416efbd
Revises: 1e5e80482bc7
Create Date: 2020-07-07 13:13:24.191425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e39d7416efbd'
down_revision = '1e5e80482bc7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ticket', sa.Column('image', sa.String(100), nullable=True))
    pass


def downgrade():
    op.drop_column('ticket', 'image')
    pass
