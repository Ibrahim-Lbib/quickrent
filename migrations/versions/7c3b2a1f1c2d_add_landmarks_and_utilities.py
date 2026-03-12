"""add landmarks and utilities

Revision ID: 7c3b2a1f1c2d
Revises: 4f15f68d43aa
Create Date: 2026-03-12

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7c3b2a1f1c2d"
down_revision = "4f15f68d43aa"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("listing", schema=None) as batch_op:
        batch_op.add_column(sa.Column("nearby_landmarks", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("has_electricity", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column("has_water", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column("has_wifi", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column("has_security", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column("has_parking", sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    with op.batch_alter_table("listing", schema=None) as batch_op:
        batch_op.drop_column("has_parking")
        batch_op.drop_column("has_security")
        batch_op.drop_column("has_wifi")
        batch_op.drop_column("has_water")
        batch_op.drop_column("has_electricity")
        batch_op.drop_column("nearby_landmarks")

