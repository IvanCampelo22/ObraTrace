from pydantic import BaseModel
from typing import Optional

class CheckListCamBase(BaseModel):
    employee_id: int 

class CheckListCamCreate(CheckListCamBase):
    qtd_cam: int = None
    qtd_box_cable: int = None
    qtd_rca: int = None
    qtd_p4: int = None
    qtd_dvr: int = None
    qtd_hd: int = None
    hds_size: int = None
    other_equipament: str = None

class ChecklistCam(CheckListCamBase):
    id: int

class CheckListCamUpdate(BaseModel):
    employee_id: Optional[int] = None
    qtd_cam: Optional[int] = None
    qtd_box_cable: Optional[int] = None
    qtd_rca: Optional[int] = None
    qtd_p4: Optional[int] = None
    qtd_dvr: Optional[int] = None
    qtd_hd: Optional[int] = None
    hds_size: Optional[int] = None
    other_equipament: Optional[str] = None