"""empty message

Revision ID: 115205e2bfc2
Revises: c20183ff7496
Create Date: 2017-06-15 11:26:49.563219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '115205e2bfc2'
down_revision = 'c20183ff7496'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consignors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column(u'users', 'goods_owner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'users', sa.Column('goods_owner_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_table('consignors')
    # ### end Alembic commands ###
