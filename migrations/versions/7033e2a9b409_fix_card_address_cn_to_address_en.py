"""Fix Card address_cn to address_en

Revision ID: 7033e2a9b409
Revises: ab995d99f031
Create Date: 2019-02-18 16:58:42.830868

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7033e2a9b409'
down_revision = 'ab995d99f031'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('address_en', sa.String(length=64), nullable=True))
    op.drop_column('cards', 'address_cn')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('address_cn', mysql.VARCHAR(collation='utf8_unicode_ci', length=64), nullable=True))
    op.drop_column('cards', 'address_en')
    # ### end Alembic commands ###
