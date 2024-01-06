from sqlalchemy import Integer, String, DateTime, Column
from sqlalchemy.sql.schema import ForeignKey
from database.conn import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class ClientAdress(Base):
    __tablename__ = 'ClientAdress'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    adress = Column(String(140), nullable=False)
    number = Column(String(20), nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(2), nullable=False)
    name_building = Column(String(120), nullable=True)
    reference_point = Column(String(340), nullable=True)
    complement = Column(String(120), nullable=True)
    updated_at = Column(DateTime, default=datetime.now())
    created_at = Column(DateTime, default=datetime.now())

    client = relationship('Client', back_populates='client_adress')
    employee = relationship('Employees', back_populates='client_adress')
    construction = relationship('Constructions',back_populates='client_adress')
    os = relationship('Os', back_populates='client_adress')
