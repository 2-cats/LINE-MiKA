"""Card add card_anime_path and card_cosplay_path

Revision ID: f30e5dc53196
Revises: 47d0e63145fe
Create Date: 2019-02-18 15:21:56.617001

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f30e5dc53196'
down_revision = '47d0e63145fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('card_anime_path', sa.String(length=64), nullable=True))
    op.add_column('cards', sa.Column('card_cosplay_path', sa.String(length=64), nullable=True))
    op.drop_column('cards', 'skin_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('skin_name', mysql.VARCHAR(collation='utf8_unicode_ci', length=64), nullable=True))
    op.drop_column('cards', 'card_cosplay_path')
    op.drop_column('cards', 'card_anime_path')
    # ### end Alembic commands ###
