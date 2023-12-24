from pydantic import BaseModel


class ConstructionBase(BaseModel):
    employee_id: int 
    client_id: int 
    client_adress_id: int 


class ConstructionCreate(ConstructionBase):
    is_done: bool = False 

class Construction(ConstructionBase):
    id: int