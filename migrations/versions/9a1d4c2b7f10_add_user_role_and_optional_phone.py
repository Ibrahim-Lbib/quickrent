"""add user role and optional phone

Revision ID: 9a1d4c2b7f10
Revises: 7c3b2a1f1c2d
Create Date: 2026-03-12

"""

from alembic import op
import sqlalchemy as sa


revision = "9a1d4c2b7f10"
down_revision = "7c3b2a1f1c2d"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("role", sa.String(length=20), nullable=False, server_default="tenant"))
        batch_op.alter_column("phone", existing_type=sa.String(length=20), nullable=True)


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("phone", existing_type=sa.String(length=20), nullable=False)
        batch_op.drop_column("role")

