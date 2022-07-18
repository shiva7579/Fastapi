"""add few columns to post

Revision ID: cd3485f72155
Revises: f0797c3a3200
Create Date: 2022-07-18 13:19:49.786758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd3485f72155'
down_revision = 'f0797c3a3200'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))                
    op.add_column('posts',sa.Column('rating',sa.Integer(),server_default="5"))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','rating')
    op.drop_column('posts','created_at')
    pass
