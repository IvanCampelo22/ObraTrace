"""add fk for tables

Revision ID: 68bf19ac3e68
Revises: 93a9314deac2
Create Date: 2023-12-08 10:13:15.785800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68bf19ac3e68'
down_revision: Union[str, None] = '93a9314deac2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('CheckListCam', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('CheckListSound', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('ClientAdress', sa.Column('client_id', sa.Integer, sa.ForeignKey('Client.id'), nullable=False))
    op.add_column('ClientAdress', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('Constructions', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('Constructions', sa.Column('client_id', sa.Integer, sa.ForeignKey('Client.id'), nullable=False))
    op.add_column('OsConstructions', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('OsConstructions',sa.Column('client_id', sa.Integer, sa.ForeignKey('Client.id'), nullable=False))
    op.add_column('OsConstructions',sa.Column('construction_id', sa.Integer, sa.ForeignKey('Constructions.id'), nullable=False))
    op.add_column('OsConstructions',sa.Column('checklist_cam_id', sa.Integer, sa.ForeignKey('CheckListCam.id'), nullable=True))
    op.add_column('OsConstructions',sa.Column('checklist_auto_id', sa.Integer, sa.ForeignKey('CheckListAuto.id'), nullable=True))       
    op.add_column('OsConstructions',sa.Column('checklist_sound_id', sa.Integer, sa.ForeignKey('CheckListSound.id'), nullable=True))
    op.add_column('OsConstructions',sa.Column('other_checklist_id', sa.Integer, sa.ForeignKey('OtherCheckList.id'), nullable=True))
    
    op.add_column('OsMaintenance', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('OsMaintenance',sa.Column('client_id', sa.Integer, sa.ForeignKey('Client.id'), nullable=False))
    op.add_column('OsMaintenance',sa.Column('client_adress_id', sa.Integer, sa.ForeignKey('ClientAdress.id'), nullable=False))
    op.add_column('OsMaintenance',sa.Column('checklist_cam_id', sa.Integer, sa.ForeignKey('CheckListCam.id'), nullable=True))
    op.add_column('OsMaintenance',sa.Column('checklist_auto_id', sa.Integer, sa.ForeignKey('CheckListAuto.id'), nullable=True))     
    op.add_column('OsMaintenance',sa.Column('checklist_sound_id', sa.Integer, sa.ForeignKey('CheckListSound.id'), nullable=True)) 
    op.add_column('OsMaintenance',sa.Column('other_checklist_id', sa.Integer, sa.ForeignKey('OtherCheckList.id'), nullable=True)) 
    
    op.add_column('OtherCheckList',sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))

def downgrade() -> None:
    pass
