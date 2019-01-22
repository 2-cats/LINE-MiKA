"""Member add arn

Revision ID: 22135cbd4b7e
Revises: 305b14fe5a0c
Create Date: 2019-01-14 17:27:03.043299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22135cbd4b7e'
down_revision = '305b14fe5a0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('arn', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('members', 'arn')
    # ### end Alembic commands ###
