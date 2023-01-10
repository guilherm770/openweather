"""create weather result table

Revision ID: f866c8b3831d
Revises: b03131bbce08
Create Date: 2023-01-09 18:12:38.585427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f866c8b3831d'
down_revision = 'b03131bbce08'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('weather_result', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('document_id', sa.Integer(), index=True, nullable=False), 
                    sa.ForeignKeyConstraint(['document_id'], ['weather_document.id'], ondelete='CASCADE'),
                    sa.Column('cityId', sa.Integer(), nullable=False),
                    sa.Column('tempCelsius', sa.Float(), nullable=False),
                    sa.Column('humidity', sa.Integer(), nullable=False)
                )
    pass

def downgrade():
    op.drop_table('weather_result')
    pass