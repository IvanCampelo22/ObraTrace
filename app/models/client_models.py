from sqlalchemy import Column, Integer, String, DateTime,Boolean
from database.conn import Base
import datetime
from sqlalchemy.orm import relationship

class Client(Base):
    __tablename__ = 'Client'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50),  nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)

    client_adress = relationship('ClientAdress', back_populates='client')
    os_construction = relationship('OsConstructions', back_populates='client')
    os = relationship('Os', back_populates='client')
    construction = relationship('Constructions', back_populates='client')


class TokenTableClient(Base):
    __tablename__ = "TokenTableClient"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)