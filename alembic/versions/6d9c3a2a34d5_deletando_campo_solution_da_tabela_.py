"""deletando campo solution da tabela OsContruction

Revision ID: 6d9c3a2a34d5
Revises: 111aca7a337d
Create Date: 2024-01-06 12:56:44.661352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d9c3a2a34d5'
down_revision: Union[str, None] = '111aca7a337d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('OsConstructions', 'solution')


def downgrade() -> None:
    pass
