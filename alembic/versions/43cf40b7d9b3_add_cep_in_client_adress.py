"""add cep in client_adress

Revision ID: 43cf40b7d9b3
Revises: 0bb62e63f49c
Create Date: 2024-01-31 21:13:54.019414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43cf40b7d9b3'
down_revision: Union[str, None] = '0bb62e63f49c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ClientAdress', sa.Column('cep', sa.String(20), nullable=False))


def downgrade() -> None:
    pass
