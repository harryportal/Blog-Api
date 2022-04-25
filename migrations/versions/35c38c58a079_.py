"""empty message

Revision ID: 35c38c58a079
Revises: b33a0e673402
Create Date: 2022-04-25 11:17:37.274820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c38c58a079'
down_revision = 'b33a0e673402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Post', sa.Column('content', sa.String(), nullable=False))
    op.drop_column('Post', 'post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Post', sa.Column('post', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('Post', 'content')
    # ### end Alembic commands ###
