"""empty message

Revision ID: 489ec8e075bd
Revises: 7f335f42192e
Create Date: 2017-06-20 17:40:10.687854

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '489ec8e075bd'
down_revision = '7f335f42192e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver_user_reg', sa.Column('use_driver_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'driver_user_reg_ibfk_1', 'driver_user_reg', type_='foreignkey')
    op.create_foreign_key(None, 'driver_user_reg', 'drivers', ['use_driver_id'], ['id'])
    op.drop_column('driver_user_reg', 'driver_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver_user_reg', sa.Column('driver_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'driver_user_reg', type_='foreignkey')
    op.create_foreign_key(u'driver_user_reg_ibfk_1', 'driver_user_reg', 'drivers', ['driver_id'], ['id'])
    op.drop_column('driver_user_reg', 'use_driver_id')
    # ### end Alembic commands ###
