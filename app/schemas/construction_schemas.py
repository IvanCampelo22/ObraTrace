from pydantic import BaseModel
from app.schemas.client_adress_schemas import ClientAdressSchema


class ConstructionBase(BaseModel):
    is_done: bool = False 


class ConstructionCreate(ConstructionBase):
    employee_id: int 
    client_id: int 
    client_adress_id: int
    

class ConstructionSchema(ConstructionBase):
    id: int 
    client_adress: ClientAdressSchema

    class Config:
        orm_mode = True

    def client_adress():
        return ClientAdressSchema

class ConstructionUpdate(ConstructionBase):
    class Config:
        orm_mode = True

