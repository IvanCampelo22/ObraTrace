from pydantic import BaseModel
from typing import Optional


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


class CheckListAutoUpdate(BaseModel):
    employee_id: Optional[int] = None
    rele_type: Optional[str] = None 
    qtd_rele: Optional[int] = None
    qtd_cable: Optional[int] = None
    switch_type: Optional[str] = None 
    qtd_switch: Optional[int] = None
    qtd_hub: Optional[int] = None
    other_equipament: Optional[str] = None