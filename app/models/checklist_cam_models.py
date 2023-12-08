from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database.conn import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class CheckListCam(Base):
    __tablename__ = 'CheckListCam'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    qtd_cam = Column(Integer, nullable=True)
    qtd_box_cable = Column(Integer, nullable=True)
    qtd_rca = Column(Integer, nullable=True)
    qtd_p4 = Column(Integer, nullable=True)
    qtd_dvr = Column(Integer, nullable=True)
    qtd_hd = Column(Integer, nullable=True)
    hds_size = Column(Integer, nullable=True)
    other_equipament = Column(String, nullable=True)
    file_budget = Column(String, nullable=True)
    update_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())

    employee_id = relationship('Employees', back_populates='checklist_cam')
    os_construction = relationship('OsConstructions', back_populates='checklist_cam_id')
    os_maintenance = relationship('OsMaintenance', back_populates='checklist_cam_id')