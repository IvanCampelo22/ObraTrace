"""create fk for checklist_auto

Revision ID: 93a9314deac2
Revises: 280c5acc2348
Create Date: 2023-12-08 09:43:24.371742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93a9314deac2'
down_revision: Union[str, None] = '280c5acc2348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('CheckListAuto', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))


def downgrade() -> None:
    pass
