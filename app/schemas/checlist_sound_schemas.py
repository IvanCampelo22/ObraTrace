from pydantic import BaseModel


class CheckListSoundBase(BaseModel):
    employee_id: int 

class ChecklistSoundCreate(CheckListSoundBase):
    qtd_sound_box: int | None = None
    qtd_cable: int | None = None
    qtd_conn: int | None = None
    qtd_ampli: int | None = None
    qtd_receiver: int | None = None
    other_equipament: str | None = None

class ChecklistSound(CheckListSoundBase):
    id: int