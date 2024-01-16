from pydantic import BaseModel
import datetime
from enum import Enum
from typing import Optional


class WorkTypeEnum(str, Enum):
    Comercial = "Comercial"
    Técnico = "Técnico"


class EmployeeBase(BaseModel):
    username: str 
    email: str 
    password: str
    work_type: WorkTypeEnum


class EmployeeCreate(EmployeeBase):
    is_active: bool


class Employee(EmployeeBase):
    id = int 


class EmployeeUpdate(BaseModel):
    username: Optional[str] = None 
    email: Optional[str] = None  
    work_type: Optional[WorkTypeEnum] = None


class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenEmployeeSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenEmployeeCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime