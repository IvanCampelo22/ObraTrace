from pydantic import BaseModel
from app.schemas.client_schemas import Client
from app.schemas.employee_schemas import Employee
import datetime

class ClientAdressBase(BaseModel):
    client_id: int
    employee_id: int
    adress: str 
    number: str 
    city: str 
    state: str 

class ClientAdressCreate(ClientAdressBase):
    name_building: str | None = None 
    reference_point: str | None = None 
    complement: str | None = None


class ClientAdress(ClientAdressBase):
    id = int

class ClientAdressUpdate(BaseModel):
    client_id: int | None = None
    employee_id: int | None = None
    adress: str | None = None
    number: str | None = None
    city: str | None = None
    state: str | None = None
    name_building: str | None = None 
    reference_point: str | None = None 
    complement: str | None = None
