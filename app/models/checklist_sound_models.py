from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database.conn import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class CheckListSound(Base):
    __tablename__ = 'CheckListSound'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    qtd_sound_box = Column(Integer, nullable=True)
    qtd_cable = Column(Integer, nullable=True)
    qtd_conn = Column(Integer, nullable=True)
    qtd_ampli = Column(Integer, nullable=True)
    qtd_receiver = Column(Integer, nullable=True)
    other_equipament = Column(String, nullable=True)
    file_budget = Column(String, nullable=True)
    update_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())

    employee_id = relationship('Employees', back_populates='checklist_cam')
    os_construction = relationship('OsContructions', back_populates='checklist_sound_id')
    os_maintenance = relationship('OsMaintenance', back_populates='checklist_sound_id')