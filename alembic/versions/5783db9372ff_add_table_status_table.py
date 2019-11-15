"""add table status table

Revision ID: 5783db9372ff
Revises: 5d8d9eba3f80
Create Date: 2019-11-15 05:24:24.846570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5783db9372ff'
down_revision = '5d8d9eba3f80'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )

def downgrade():
    op.drop_table('status')
