from pydantic import BaseModel
from typing import Optional

class OtherCheckListBase(BaseModel):
    employee_id: int 

class OtherCheckListCreate(OtherCheckListBase):
    equipment: str
    file_budget: str

class OtherCheckListSchema(OtherCheckListBase):
    id: int

class OtherCheckListUpdate(BaseModel):
    employee_id: Optional[int] = None
    equipment: Optional[str] = None 
    file_budget: Optional[str] = None