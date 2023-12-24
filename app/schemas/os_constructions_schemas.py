from pydantic import BaseModel
from datetime import date


class OsConstructionsBase(BaseModel):
    employee_id: int 
    client_id: int 
    construction_id: int

class OsConstructionsCreate(OsConstructionsBase):
    checklist_cam_id: int
    checklist_auto_id: int
    checklist_sound_id: int
    other_checklist_id: int
    image: str
    scheduling: date
    end_date: date
    info: str
    solution: str
    sale: str
    signature_emplooye = str
    signature_client = str

class OsConstructions:
    id: int