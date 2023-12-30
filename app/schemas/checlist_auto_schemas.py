from pydantic import BaseModel


class CheckListAutoBase(BaseModel):
    employee_id: int 


class CheckListAutoCreate(CheckListAutoBase):
    rele_type: str = None 
    qtd_rele: int = None
    qtd_cable: int = None
    switch_type: str = None 
    qtd_switch: int = None
    qtd_hub: int = None
    other_equipament: str = None
    

class CheckListAuto(CheckListAutoBase):
    id: int 
