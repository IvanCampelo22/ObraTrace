from pydantic import BaseModel
from typing import Optional

class ConstructionBase(BaseModel):
    is_done: Optional[bool] = False 


class ConstructionCreate(ConstructionBase):
    employee_id: int 
    client_id: int 
    client_adress_id: int
    

class ConstructionSchema(ConstructionBase):
    id: int 

    class Config:
        orm_mode = True


class ConstructionUpdate(ConstructionBase):
    employee_id: Optional[int] = None  
    client_id: Optional[int] = None 
    client_adress_id: Optional[int] = None 

    class Config:
        orm_mode = True

