"""adicionando os_type à tabela os

Revision ID: 0bb62e63f49c
Revises: 6d9c3a2a34d5
Create Date: 2024-01-06 13:26:44.429090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bb62e63f49c'
down_revision: Union[str, None] = '6d9c3a2a34d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE os_type_enum AS ENUM ('Instalação', 'Manutenção')")
    op.add_column('Os', sa.Column('os_type', sa.Enum('Instalação', 'Manutenção', name='os_type_enum'), nullable=False, server_default='Instalação'))


def downgrade() -> None:
    pass
