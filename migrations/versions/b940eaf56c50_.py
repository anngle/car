"""empty message

Revision ID: b940eaf56c50
Revises: 164d37ae7ab4
Create Date: 2017-07-21 11:14:13.575968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b940eaf56c50'
down_revision = '164d37ae7ab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('make_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goods', 'make_count')
    # ### end Alembic commands ###
