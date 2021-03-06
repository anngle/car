"""empty message

Revision ID: f5df6852ec8a
Revises: 03d942d156f4
Create Date: 2017-10-13 00:46:56.773512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5df6852ec8a'
down_revision = '03d942d156f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('haoyoutuijians',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tuijianren', sa.Integer(), nullable=True),
    sa.Column('beituijianren', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'consignor_images', 'consignors', ['consignor_id'], ['id'])
    op.create_foreign_key(None, 'couponsion', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'driver_self_orders', 'goods', ['goods_id'], ['id'])
    op.create_foreign_key(None, 'driver_self_orders', 'drivers', ['driver_id'], ['id'])
    op.create_foreign_key(None, 'positions', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'tixianchengqings', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tixianchengqings', type_='foreignkey')
    op.drop_constraint(None, 'positions', type_='foreignkey')
    op.drop_constraint(None, 'driver_self_orders', type_='foreignkey')
    op.drop_constraint(None, 'driver_self_orders', type_='foreignkey')
    op.drop_constraint(None, 'couponsion', type_='foreignkey')
    op.drop_constraint(None, 'consignor_images', type_='foreignkey')
    op.drop_table('haoyoutuijians')
    # ### end Alembic commands ###
