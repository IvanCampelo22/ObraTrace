from pydantic import BaseModel
from datetime import date
from typing import Optional


class OsConstructionsBase(BaseModel):
    employee_id: int 
    client_id: int 
    construction_id: int
    

class OsConstructionsCreate(OsConstructionsBase):
    checklist: Optional[str] = None
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
    checklist: Optional[str] = None
    scheduling: Optional[date] = None 
    end_date: Optional[date] = None
    info: Optional[str] = None
    solution: Optional[str] = None 
    sale: Optional[str] = None
    signature_emplooye: Optional[str] = None 
    signature_client: Optional[str] = None