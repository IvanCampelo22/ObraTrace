"""fk

Revision ID: 280c5acc2348
Revises: d7d393d2aaf2
Create Date: 2023-12-08 09:39:09.252405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '280c5acc2348'
down_revision: Union[str, None] = 'd7d393d2aaf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
    # ### end Alembic commands ###
