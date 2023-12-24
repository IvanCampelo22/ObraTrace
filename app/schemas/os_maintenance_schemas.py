from pydantic import BaseModel
from datetime import date
from typing import Optional


class OsMaintenanceBase(BaseModel):
    employee_id: int 
    client_id: int 
    client_adress_id: int

class OsMaintenanceCreate(OsMaintenanceBase):
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

class OsMaintenance:
    id: int