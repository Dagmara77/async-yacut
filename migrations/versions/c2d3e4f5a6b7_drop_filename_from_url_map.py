"""Drop filename column from url_map

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-07-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d3e4f5a6b7'
down_revision = 'b1c2d3e4f5a6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_column('filename')


def downgrade():
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('filename', sa.String(length=256), nullable=True)
        )
