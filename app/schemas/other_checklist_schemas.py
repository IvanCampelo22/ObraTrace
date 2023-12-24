from pydantic import BaseModel


class OtherCheckListBase(BaseModel):
    employee_id: int 

class OtherCheckListCreate(OtherCheckListBase):
    equipment: str
    file_budget: str

class OtherCheckList(OtherCheckListBase):
    id: int