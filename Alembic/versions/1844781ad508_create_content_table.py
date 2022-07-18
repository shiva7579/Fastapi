"""create content table

Revision ID: 1844781ad508
Revises: 3bdd97641f10
Create Date: 2022-07-17 16:03:35.205051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1844781ad508'
down_revision = '3bdd97641f10'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
