"""empty message

Revision ID: 1896aacea1be
Revises: 87ff2ca8b270
Create Date: 2017-09-10 11:13:09.898220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1896aacea1be'
down_revision = '87ff2ca8b270'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'positions', 'users', ['users'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'positions', type_='foreignkey')
    # ### end Alembic commands ###
