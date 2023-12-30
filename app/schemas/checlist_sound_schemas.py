from pydantic import BaseModel


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