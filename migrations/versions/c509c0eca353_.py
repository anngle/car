"""empty message

Revision ID: c509c0eca353
Revises: 7fb0e45b8abe
Create Date: 2017-06-20 11:20:29.004352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c509c0eca353'
down_revision = '7fb0e45b8abe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_pays',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order', sa.String(length=20), nullable=True),
    sa.Column('goods_id', sa.Integer(), nullable=True),
    sa.Column('drivers_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('pay_time', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('pay_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['drivers_id'], ['drivers.id'], ),
    sa.ForeignKeyConstraint(['goods_id'], ['goods.id'], ),
    sa.ForeignKeyConstraint(['pay_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order')
    )
    op.add_column(u'user_msgs', sa.Column('show', sa.Integer(), nullable=True))
    op.add_column(u'user_msgs', sa.Column('state', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'user_msgs', 'state')
    op.drop_column(u'user_msgs', 'show')
    op.drop_table('order_pays')
    # ### end Alembic commands ###
