"""empty message

Revision ID: ccafc0093c8b
Revises: cfd1d743ef66
Create Date: 2017-07-11 10:51:50.493726

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ccafc0093c8b'
down_revision = 'cfd1d743ef66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'driver_posts_ibfk_1', 'driver_posts', type_='foreignkey')
    op.create_foreign_key(None, 'driver_posts', 'goods', ['consignor_user_id'], ['id'])
    op.add_column('goods', sa.Column('consignors_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'goods_ibfk_2', 'goods', type_='foreignkey')
    op.create_foreign_key(None, 'goods', 'consignors', ['consignors_id'], ['id'])
    op.drop_column('goods', 'user_id')
    op.drop_constraint(u'order_pays_ibfk_1', 'order_pays', type_='foreignkey')
    op.drop_column('order_pays', 'drivers_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_pays', sa.Column('drivers_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'order_pays_ibfk_1', 'order_pays', 'drivers', ['drivers_id'], ['id'])
    op.add_column('goods', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'goods', type_='foreignkey')
    op.create_foreign_key(u'goods_ibfk_2', 'goods', 'users', ['user_id'], ['id'])
    op.drop_column('goods', 'consignors_id')
    op.drop_constraint(None, 'driver_posts', type_='foreignkey')
    op.create_foreign_key(u'driver_posts_ibfk_1', 'driver_posts', 'consignors', ['consignor_user_id'], ['id'])
    # ### end Alembic commands ###
