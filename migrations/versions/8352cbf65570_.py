"""empty message

Revision ID: 8352cbf65570
Revises: b940eaf56c50
Create Date: 2017-07-24 15:55:48.717868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8352cbf65570'
down_revision = 'b940eaf56c50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('show_statie', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goods', 'show_statie')
    # ### end Alembic commands ###
