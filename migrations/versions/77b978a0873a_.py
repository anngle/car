"""empty message

Revision ID: 77b978a0873a
Revises: da6e39764401
Create Date: 2017-07-21 08:59:52.571403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77b978a0873a'
down_revision = 'da6e39764401'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_infos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('length', sa.String(length=80), nullable=True),
    sa.Column('tiji', sa.String(length=80), nullable=True),
    sa.Column('zhongliang', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car_infos')
    # ### end Alembic commands ###
