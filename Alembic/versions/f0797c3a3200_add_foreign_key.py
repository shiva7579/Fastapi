"""add foreign key

Revision ID: f0797c3a3200
Revises: fa39a0400d77
Create Date: 2022-07-18 13:04:17.718090

"""
from urllib.request import OpenerDirector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0797c3a3200'
down_revision = 'fa39a0400d77'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post-user-fk',source_table="posts",referent_table="users",local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post-user-fk',table_name="posts")
    op.drop_column('posts','user_id')
    pass
