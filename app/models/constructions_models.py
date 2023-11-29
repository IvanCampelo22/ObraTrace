from sqlalchemy import Column, Integer, String, DateTime,Boolean, ForeignKey
from database.conn import Base
import datetime
from sqlalchemy.orm import relationship

class Constructions(Base):
    __tablename__ = 'Constructions'

    id = Column(Integer, primary_key=True, index=True)
    employees_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)
    client_adress_id = Column(Integer, ForeignKey('ClientAdress.id'), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_done = Column(Boolean, default=False)

    os_construction = relationship('OsConstructions', back_populates='construction')
    client = relationship('Client', back_populates='construction')
    employee = relationship('Employees', back_populates='construction')
    
