from sqlalchemy import Column, Integer, String, DateTime,Boolean, Enum
from sqlalchemy.orm import relationship
from database.conn import Base
import datetime

class Employees(Base):
    __tablename__ = 'Client'
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
    construction = relationship('Construction', back_populates='employee')
    other_checklist = relationship('OtherCheckList', back_populates='employee')

class TokenTableEmployees(Base):
    __tablename__ = "TokenTableEmployees"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)