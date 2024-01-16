from pydantic import BaseModel
from datetime import date
from typing import Optional


class OsConstructionsBase(BaseModel):
    employee_id: int 
    client_id: int 
    construction_id: int
    

class OsConstructionsCreate(OsConstructionsBase):
    checklist_cam_id: int
    checklist_auto_id: int
    checklist_sound_id: int
    other_checklist_id: int
    scheduling: Optional[date] = None 
    end_date: Optional[date] = None
    info: str
    solution: str
    sale: str
    signature_emplooye: str
    signature_client: str


class OsConstructions:
    id: int


class OsConstructionsUpdate(BaseModel): 
    employee_id: Optional[int] = None
    client_id: Optional[int] = None  
    construction_id: Optional[int] = None
    checklist_cam_id: Optional[int] = None 
    checklist_auto_id: Optional[int] = None 
    checklist_sound_id: Optional[int] = None 
    other_checklist_id: Optional[int] = None 
    scheduling: Optional[date] = None 
    end_date: Optional[date] = None
    info: Optional[str] = None
    solution: Optional[str] = None 
    sale: Optional[str] = None
    signature_emplooye: Optional[str] = None 
    signature_client: Optional[str] = None