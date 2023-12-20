from pydantic import BaseModel


class CheckListCamBase(BaseModel):
    employee_id: int 

class CheckListCamCreate(CheckListCamBase):
    qtd_cam: int | None = None
    qtd_box_cable: int | None = None
    qtd_rca: int | None = None
    qtd_p4: int | None = None
    qtd_dvr: int | None = None
    qtd_hd: int | None = None
    hds_size: int | None = None
    other_equipament: str | None = None

class ChecklistCam(CheckListCamBase):
    id: int