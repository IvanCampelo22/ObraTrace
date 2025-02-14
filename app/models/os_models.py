from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from database.conn import Base
import datetime

class Os(Base):
    __tablename__ = 'Os'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employees.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('Client.id'), nullable=False)
    client_adress_id = Column(Integer, ForeignKey('ClientAdress.id'), nullable=False)
    checklist = Column(String, nullable=True)
    image = Column(String, nullable=True)
    os_type = Column(Enum('Instalação', 'Manutenção', name='os_type_enum'), nullable=False)
    scheduling = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    info = Column(String, nullable=True)
    solution = Column(String, nullable=True)
    sale = Column(String, nullable=True)
    signature_emplooye = Column(String(120), nullable=True)
    signature_client = Column(String(120), nullable=True)
    update_at = Column(DateTime, default=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)

    employee = relationship('Employees', back_populates='os')
    client = relationship('Client', back_populates='os')
    client_adress = relationship('ClientAdress', back_populates='os')
    
