from pydantic import BaseModel


class CheckListAutoBase(BaseModel):
    employee_id: int 


class CheckListAutoCreate(CheckListAutoBase):
    rele_type: str | None = None
    qtd_rele: int | None = None 
    qtd_cable: int | None = None 
    switch_type: str | None = None 
    qtd_switch: int | None = None 
    qtd_hub: int | None = None 
    other_equipament: str | None = None
    

class CheckListAuto(CheckListAutoBase):
    id: int 
