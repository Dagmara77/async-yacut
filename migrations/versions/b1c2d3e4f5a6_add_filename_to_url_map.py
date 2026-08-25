"""Add filename column to url_map

Revision ID: b1c2d3e4f5a6
Revises: da50bd118283
Create Date: 2026-07-03 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c2d3e4f5a6'
down_revision = 'da50bd118283'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('filename', sa.String(length=256), nullable=True)
        )


def downgrade():
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_column('filename')
