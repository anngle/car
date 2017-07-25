"""empty message

Revision ID: debc3bca199a
Revises: ccafc0093c8b
Create Date: 2017-07-19 09:49:53.026947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'debc3bca199a'
down_revision = 'ccafc0093c8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver_posts', sa.Column('end_qu', sa.String(length=100), nullable=True))
    op.add_column('driver_posts', sa.Column('end_sheng', sa.String(length=100), nullable=True))
    op.add_column('driver_posts', sa.Column('end_shi', sa.String(length=100), nullable=True))
    op.add_column('driver_posts', sa.Column('start_qu', sa.String(length=100), nullable=True))
    op.add_column('driver_posts', sa.Column('start_sheng', sa.String(length=100), nullable=True))
    op.add_column('driver_posts', sa.Column('start_shi', sa.String(length=100), nullable=True))
    op.add_column('driver_posts', sa.Column('zone', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('driver_posts', 'zone')
    op.drop_column('driver_posts', 'start_shi')
    op.drop_column('driver_posts', 'start_sheng')
    op.drop_column('driver_posts', 'start_qu')
    op.drop_column('driver_posts', 'end_shi')
    op.drop_column('driver_posts', 'end_sheng')
    op.drop_column('driver_posts', 'end_qu')
    # ### end Alembic commands ###
