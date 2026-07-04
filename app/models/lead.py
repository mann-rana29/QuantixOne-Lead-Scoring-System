from pydantic import BaseModel, EmailStr
from datetime import datetime

class LeadBase(BaseModel):
    workspace_id : str
    name : str
    email: EmailStr
    company : str
    job_title : str
    industry : str
    company_size : int
    source : str
    status : str = "active"

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id : str
    created_at : datetime

class LeadUpdate(BaseModel):
    workspace_id : str | None = None
    name : str | None = None
    email: EmailStr | None = None
    company : str | None = None
    job_title : str | None = None
    industry : str | None = None
    company_size : int | None = None
    source : str | None = None
    status : str | None = None