"""add column client_adress_id in contructions table

Revision ID: 46e761a641e0
Revises: 68bf19ac3e68
Create Date: 2023-12-23 23:12:41.896645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46e761a641e0'
down_revision: Union[str, None] = '68bf19ac3e68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Constructions', sa.Column('client_adress_id', sa.Integer, sa.ForeignKey('ClientAdress.id'), nullable=False))


def downgrade() -> None:
    pass
