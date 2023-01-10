"""create weather document table

Revision ID: b03131bbce08
Revises: 
Create Date: 2023-01-09 18:11:41.523938

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from openweather.models import ProcessingStatusType


# revision identifiers, used by Alembic.
revision = 'b03131bbce08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('weather_document', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
                    sa.Column('status', sa.Enum(ProcessingStatusType), default=ProcessingStatusType.waiting, nullable=False, index=True),
                    sa.Column('error_message', sa.Text(), nullable=True)
                )
    pass

def downgrade():
    op.drop_table('weather_document')
    pass