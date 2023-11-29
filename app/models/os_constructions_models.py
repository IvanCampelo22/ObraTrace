from sqlalchemy import Column, Integer, String, DateTime,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base
import datetime

class OsConstructions(Base):
    __tablename__ = 'OsConstructions'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)
    constructions_id = Column(Integer, ForeignKey('Contructions.id'), nullable=False)
    checklist_cam_id = Column(Integer, ForeignKey('CheckListCam.id'), nullable=True)
    checklist_auto_id = Column(Integer, ForeignKey('CheckListAuto.id'), nullable=True)
    checklist_sound_id = Column(Integer, ForeignKey('CheckListSound.id'), nullable=True)
    checklist_other_id = Column(Integer, ForeignKey('OtherCheckList'), nullable=True)
    image = Column(String, nullable=True)
    scheduling = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    info = Column(String, nullable=True)
    solution = Column(String, nullable=True)
    signature_emplooye = Column(String(120), nullable=True)
    signature_client = Column(String(120), nullable=True)
    update_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)

    employee = relationship('Employees', back_populates='os_construction')
    client = relationship('Client', back_populates='os_construction')
    construction = relationship('Constructions', back_populates='os_construction')
    other_checklist = relationship('OtherCheckList', back_populates='os_construction')
    
