"""empty message

Revision ID: c5ac42d66ce3
Revises: 354a631846c7
Create Date: 2017-06-14 10:28:04.723551

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c5ac42d66ce3'
down_revision = '354a631846c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('drivers', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('drivers', sa.Column('phone', mysql.VARCHAR(length=20), nullable=True))
    # ### end Alembic commands ###
