"""empty message

Revision ID: 830a0f41849b
Revises: 77b978a0873a
Create Date: 2017-07-21 09:01:41.383141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '830a0f41849b'
down_revision = '77b978a0873a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car_infos', sa.Column('sort', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car_infos', 'sort')
    # ### end Alembic commands ###
