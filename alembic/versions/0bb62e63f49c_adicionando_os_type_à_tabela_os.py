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
    op.create_table('Os',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('scheduling', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('solution', sa.String(), nullable=True),
    sa.Column('sale', sa.String(), nullable=True),
    sa.Column('signature_emplooye', sa.String(length=120), nullable=True),
    sa.Column('signature_client', sa.String(length=120), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute("CREATE TYPE os_type_enum AS ENUM ('Instalação', 'Manutenção')")
    op.add_column('Os', sa.Column('os_type', sa.Enum('Instalação', 'Manutenção', name='os_type_enum'), nullable=False, server_default='Instalação'))
    op.add_column('Os', sa.Column('employee_id', sa.Integer, sa.ForeignKey('Employees.id'), nullable=False))
    op.add_column('Os',sa.Column('client_id', sa.Integer, sa.ForeignKey('Client.id'), nullable=False))
    op.add_column('Os',sa.Column('client_adress_id', sa.Integer, sa.ForeignKey('ClientAdress.id'), nullable=False))
    op.add_column('Os',sa.Column('checklist_cam_id', sa.Integer, sa.ForeignKey('CheckListCam.id'), nullable=True))
    op.add_column('Os',sa.Column('checklist_auto_id', sa.Integer, sa.ForeignKey('CheckListAuto.id'), nullable=True))     
    op.add_column('Os',sa.Column('checklist_sound_id', sa.Integer, sa.ForeignKey('CheckListSound.id'), nullable=True)) 
    op.add_column('Os',sa.Column('other_checklist_id', sa.Integer, sa.ForeignKey('OtherCheckList.id'), nullable=True)) 

def downgrade() -> None:
    op.drop_table('OsMaintenance')
