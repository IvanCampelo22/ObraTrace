from pydantic import BaseModel


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