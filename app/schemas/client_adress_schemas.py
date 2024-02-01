from pydantic import BaseModel
from app.schemas.client_schemas import Client
from app.schemas.employee_schemas import Employee
from typing import Optional 


class ClientAdressBase(BaseModel):
    client_id: int
    employee_id: int
    adress: str 
    number: str 
    cep: str
    city: str 
    state: str 

class ClientAdressCreate(ClientAdressBase):
    name_building: str = None
    reference_point: str = None
    complement: str = None


class ClientAdressSchema(BaseModel):
    id = int
    name_building: str = None
    reference_point: str = None
    complement: str = None

    class Config:
        orm_mode = True
        

class ClientAdressUpdate(BaseModel):
    client_id: Optional[int] = None 
    employee_id: Optional[int] = None 
    adress: Optional[str] = None  
    number: Optional[str] = None 
    cep: Optional[str] = None 
    city: Optional[str] = None  
    state: Optional[str] = None  
    name_building: Optional[str] = None
    reference_point: Optional[str] = None
    complement: Optional[str] = None
