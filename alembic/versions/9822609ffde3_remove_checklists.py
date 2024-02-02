"""remove checklists

Revision ID: 9822609ffde3
Revises: 96b0477dd8d4
Create Date: 2024-02-02 08:35:22.325926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9822609ffde3'
down_revision: Union[str, None] = '96b0477dd8d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('Os', 'checklist_cam_id')
    op.drop_column('Os', 'checklist_auto_id')
    op.drop_column('Os', 'checklist_sound_id')
    op.drop_column('Os', 'other_checklist_id')
    op.drop_column('OsConstructions', 'checklist_cam_id')
    op.drop_column('OsConstructions', 'checklist_auto_id')
    op.drop_column('OsConstructions', 'checklist_sound_id')
    op.drop_column('OsConstructions', 'other_checklist_id')
    op.drop_table('OsMaintenance')
    op.drop_table('CheckListCam')
    op.drop_table('CheckListSound')
    op.drop_table('CheckListAuto')
    op.drop_table('OtherCheckList')


def downgrade() -> None:
    pass
