"""Add member arn

Revision ID: 216d42d7a4f4
Revises: e131410d0998
Create Date: 2019-01-17 15:50:51.729590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '216d42d7a4f4'
down_revision = 'e131410d0998'
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
