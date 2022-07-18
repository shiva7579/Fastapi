"""create users table

Revision ID: fa39a0400d77
Revises: 1844781ad508
Create Date: 2022-07-17 16:17:17.971806

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa39a0400d77'
down_revision = '1844781ad508'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',sa.Column('id',sa.INTEGER(), nullable=False,primary_key=True),sa.Column('email',sa.String(), nullable=False,unique=True),
                    sa.Column('password',sa.String(),nullable=False),sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'),nullable=False))
    pass




def downgrade():
    op.drop_table('users')
    pass
