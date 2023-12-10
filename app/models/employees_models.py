from sqlalchemy import Column, Integer, String, DateTime,Boolean, Enum
from sqlalchemy.orm import relationship
from database.conn import Base
import datetime
from app.models.os_maintenance_models import OsMaintenance
from app.models.other_checklist_models import OtherCheckList
from app.models.checklist_auto_models import CheckListAuto
from app.models.checklist_cam_models import CheckListCam
from app.models.checklist_sound_models import CheckListSound

class Employees(Base):
    __tablename__ = 'Employees'
    id = Column(Integer, primary_key=True)
    username = Column(String(50),  nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    work_type = Column(Enum('Comercial', 'Técnico', name='work_type_enum'), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)

    client_adress = relationship('ClientAdress', back_populates='employee') 
    os_construction = relationship('OsConstructions', back_populates='employee')
    os_maintenance = relationship('OsMaintenance', back_populates='employee')
    construction = relationship('Constructions', back_populates='employee')
    other_checklist = relationship('OtherCheckList', back_populates='employee')
    checklist_cam = relationship('CheckListCam', back_populates='employee')
    checklist_auto = relationship('CheckListAuto', back_populates='employee')  # Renomeado para evitar conflito com 'checklist_auto'
    checklist_sound = relationship('CheckListSound', back_populates='employee')

class TokenTableEmployees(Base):
    __tablename__ = "TokenTableEmployees"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)