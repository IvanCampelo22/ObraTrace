"""add column client_adress_id in contructions table

Revision ID: 111aca7a337d
Revises: 46e761a641e0
Create Date: 2023-12-23 23:16:49.133575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '111aca7a337d'
down_revision: Union[str, None] = '46e761a641e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
