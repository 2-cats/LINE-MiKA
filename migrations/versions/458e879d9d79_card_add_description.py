"""Card add description

Revision ID: 458e879d9d79
Revises: 7033e2a9b409
Create Date: 2019-02-22 09:32:32.811887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '458e879d9d79'
down_revision = '7033e2a9b409'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('description', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cards', 'description')
    # ### end Alembic commands ###
