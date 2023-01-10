"""create schemas

Revision ID: 39ff65096a9e
Revises: 
Create Date: 2023-01-09 17:57:52.667370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39ff65096a9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create database openweather_producao")
    op.execute("create database openweather_homologacao")

def downgrade():
    op.execute("drop database openweather_producao")
    op.execute("drop database openweather_homologacao")