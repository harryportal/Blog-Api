"""empty message

Revision ID: 3fc2c633e2f6
Revises: dcec0ea3eac2
Create Date: 2022-04-28 12:42:41.748576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fc2c633e2f6'
down_revision = 'dcec0ea3eac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'User', ['username'])
    op.create_unique_constraint(None, 'User', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'User', type_='unique')
    op.drop_constraint(None, 'User', type_='unique')
    # ### end Alembic commands ###