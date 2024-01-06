from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class OsTypeEnum(str, Enum):
    Instalação = "Instalação"
    Manutenção = "Manutenção"

class OsBase(BaseModel):
    employee_id: int 
    client_id: int 
    client_adress_id: int
    os_type: OsTypeEnum

class OsCreate(OsBase):
    checklist_cam_id: Optional[int] = None
    checklist_auto_id: Optional[int] = None 
    checklist_sound_id: Optional[int] = None 
    other_checklist_id: Optional[int] = None
    scheduling: Optional[date] = None 
    end_date: Optional[date] = None
    info: str
    solution: str
    sale: str
    signature_emplooye: str
    signature_client: str

class Os:
    id: int