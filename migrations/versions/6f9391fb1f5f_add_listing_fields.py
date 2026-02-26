"""add listing fields

Revision ID: 6f9391fb1f5f
Revises: 
Create Date: 2026-02-18 01:36:30.732233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6f9391fb1f5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop dependent foreign keys FIRST (before dropping tables)
    op.drop_constraint('listing_category_id_fkey', 'listing', type_='foreignkey')
    op.drop_constraint('listing_location_id_fkey', 'listing', type_='foreignkey')

    # Now safe to drop the no-longer-needed tables
    op.drop_table('category')
    op.drop_table('location')

    # Alter the listing table
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('bedrooms', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('bathrooms', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('whatsapp', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

        # These should already be dropped above, but if Alembic insists, keep only if needed
        # (you can safely REMOVE these two lines now)
        # batch_op.drop_constraint(batch_op.f('listing_location_id_fkey'), type_='foreignkey')
        # batch_op.drop_constraint(batch_op.f('listing_category_id_fkey'), type_='foreignkey')

        batch_op.drop_column('category_id')
        batch_op.drop_column('location_id')
        batch_op.drop_column('create_at')   # old typo column

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.drop_column('create_at')   # old typo column
        
    # ### end Alembic commands ###


def downgrade():
    # 1. Recreate dropped tables FIRST
    op.create_table('location',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Restore columns and constraints on listing
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_at', sa.DateTime(), nullable=True))  # old name
        batch_op.add_column(sa.Column('location_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))

        batch_op.create_foreign_key(
            'listing_location_id_fkey',
            'location',
            ['location_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'listing_category_id_fkey',
            'category',
            ['category_id'],
            ['id']
        )

        # Remove new columns
        batch_op.drop_column('created_at')
        batch_op.drop_column('whatsapp')
        batch_op.drop_column('location')   # the new string column
        batch_op.drop_column('bathrooms')
        batch_op.drop_column('bedrooms')
        batch_op.drop_column('type')

    # 3. Restore user table old column
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_at', sa.DateTime(), nullable=True))
        batch_op.drop_column('created_at')
        
    # ### end Alembic commands ###
