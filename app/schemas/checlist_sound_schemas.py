from pydantic import BaseModel
from typing import Optional

class CheckListSoundBase(BaseModel):
    employee_id: int 

class CheckListSoundCreate(CheckListSoundBase):
    qtd_sound_box: int = None
    qtd_cable: int = None
    qtd_conn: int = None
    qtd_ampli: int = None
    qtd_receiver: int = None
    other_equipament: str = None
    file_budget: str = None

class ChecklistSound(CheckListSoundBase):
    id: int


class CheckListSoundUpdate(BaseModel):
    employee_id: Optional[int] = None 
    qtd_sound_box: Optional[int] = None
    qtd_cable: Optional[int] = None
    qtd_conn: Optional[int] = None
    qtd_ampli: Optional[int] = None
    qtd_receiver: Optional[int] = None
    other_equipament: Optional[str] = None
    file_budget: Optional[str] = None
