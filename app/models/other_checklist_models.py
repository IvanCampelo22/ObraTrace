from sqlalchemy import Column, Integer, String, DateTime,Boolean 
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base
import datetime

class OtherCheckList(Base):
    __tablename__ = 'OtherCheckList'

    id = Column(Integer, primary_key=True, nullable=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    equipment = Column(String, nullable=True)
    file_budget = Column(String, nullable=True)
    update_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)

    employee = relationship('Employees', back_populates='other_checklist')
    os_construction = relationship('OsConstructions', back_populates='other_checklist')
    os_maintenance = relationship('OsMaintenance', back_populates='other_checklist')
