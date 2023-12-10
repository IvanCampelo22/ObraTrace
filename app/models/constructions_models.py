from sqlalchemy import Column, Integer, String, DateTime,Boolean
from database.conn import Base
import datetime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from app.models.client_adress_models import ClientAdress

class Constructions(Base):
    __tablename__ = 'Constructions'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)
    client_adress_id = Column(Integer, ForeignKey('ClientAdress.id'), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_done = Column(Boolean, default=False)

    os_construction = relationship('OsConstructions', back_populates='construction')
    client_adress = relationship('ClientAdress', back_populates='construction')
    client = relationship('Client', back_populates='construction')
    employee = relationship('Employees', back_populates='construction')
    
