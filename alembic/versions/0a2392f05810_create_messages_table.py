"""create messages table

Revision ID: 0a2392f05810
Revises: 9dbc7d2409e8
Create Date: 2019-11-14 04:29:26.925655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a2392f05810'
down_revision = '9dbc7d2409e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Unicode(500), nullable=False),
        sa.Column('userId', sa.String(50), nullable=False),
        sa.Column('sentBy', sa.String(50), nullable=False),
        sa.Column('sentTo', sa.String(50), nullable=False)
        )


def downgrade():
    op.drop_table('messages')
