"""create cityIds table

Revision ID: c91f4a974dc3
Revises: f866c8b3831d
Create Date: 2023-01-09 18:13:04.543317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c91f4a974dc3'
down_revision = 'f866c8b3831d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cityIds', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('cityId', sa.Integer(), nullable=False)
                )
    pass

def downgrade():
    op.drop_table('cityIds')
    pass