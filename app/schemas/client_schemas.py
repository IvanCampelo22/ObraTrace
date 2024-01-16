from pydantic import BaseModel
from typing import Optional
import datetime

class ClientBase(BaseModel):
    username: str 
    email: str 
    password: str

class ClientCreate(ClientBase):
    is_active: bool

class Client(ClientBase):
    id: int 


class ClientUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None 

class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenClientSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenClientCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime