from sqlalchemy import Column, Integer, String, DateTime
from database.conn import Base 
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
from app.models.os_constructions_models import OsConstructions

class CheckListAuto(Base):
    __tablename__ = 'CheckListAuto'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    rele_type = Column(String(120), nullable=True)
    qtd_rele = Column(Integer, nullable=True)
    qtd_cable = Column(Integer, nullable=True)
    switch_type = Column(String(120), nullable=True)
    qtd_switch = Column(Integer, nullable=True)
    qtd_hub = Column(Integer, nullable=True)
    other_equipament = Column(String, nullable=True) 
    file_budget = Column(String, nullable=True)
    update_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())

    employee = relationship('Employees', back_populates='checklist_auto')
    os_construction = relationship('OsConstructions', back_populates='checklist_auto')  
    os = relationship('Os', back_populates='checklist_auto')