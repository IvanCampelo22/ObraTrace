from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base
import datetime
from app.models.constructions_models import Constructions
from app.models.other_checklist_models import OtherCheckList

class OsConstructions(Base):
    __tablename__ = 'OsConstructions'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)
    construction_id = Column(Integer, ForeignKey('Constructions.id'), nullable=False)
    checklist_cam_id = Column(Integer, ForeignKey('CheckListCam.id'), nullable=True)
    checklist_auto_id = Column(Integer, ForeignKey('CheckListAuto.id'), nullable=True)
    checklist_sound_id = Column(Integer, ForeignKey('CheckListSound.id'), nullable=True)
    other_checklist_id  = Column(Integer, ForeignKey('OtherCheckList.id'), nullable=True)
    image = Column(String, nullable=True)
    scheduling = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    info = Column(String, nullable=True)
    sale = Column(String, nullable=True)
    signature_emplooye = Column(String(120), nullable=True)
    signature_client = Column(String(120), nullable=True)
    update_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)

    employee = relationship('Employees', back_populates='os_construction')  # Renomeado para evitar conflito com 'employee_id'
    client = relationship('Client', back_populates='os_construction')
    construction = relationship('Constructions', back_populates='os_construction')
    other_checklist = relationship('OtherCheckList', back_populates='os_construction')
    checklist_cam = relationship('CheckListCam', back_populates='os_construction')
    checklist_auto = relationship('CheckListAuto', back_populates='os_construction')
    checklist_sound = relationship('CheckListSound', back_populates='os_construction')
