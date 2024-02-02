"""remove checklists and add hour in scheduling

Revision ID: 96b0477dd8d4
Revises: 43cf40b7d9b3
Create Date: 2024-02-02 07:59:48.872451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96b0477dd8d4'
down_revision: Union[str, None] = '43cf40b7d9b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Os', sa.Column('checklist', sa.String, nullable=True))
    op.alter_column('Os', sa.Column('scheduling', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('Os', sa.Column('end_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('OsConstructions', sa.Column('checklist', sa.String, nullable=True))
    op.alter_column('OsConstructions', sa.Column('scheduling', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('OsConstructions', sa.Column('end_date', sa.DateTime(timezone=True), nullable=True))

def downgrade() -> None:
    op.drop_column('Os', sa.Column('checklist_cam_id'))
    op.drop_column('Os', sa.Column('checklist_auto_id'))
    op.drop_column('Os', sa.Column('checklist_sound_id'))
    op.drop_column('Os', sa.Column('other_checklist_id'))
    op.drop_column('OsConstructions', sa.Column('checklist_cam_id'))
    op.drop_column('OsConstructions', sa.Column('checklist_auto_id'))
    op.drop_column('OsConstructions', sa.Column('checklist_sound_id'))
    op.drop_column('OsConstructions', sa.Column('other_checklist_id'))
    op.drop_table('OsMaintenance')
    op.drop_table('CheckListCam')
    op.drop_table('CheckListSound')
    op.drop_table('CheckListAuto')
    op.drop_table('OtherCheckList')