from pydantic import BaseModel
from datetime import datetime

class CompanySizeRange(BaseModel):
    min : int
    max : int

class PersonaBase(BaseModel):
    workspace_id : str
    name : str
    job_titles : list[str] = []
    industries : list[str] = []
    company_size_range : CompanySizeRange | None = None
    lead_source : str | None = None
    model_id : str #references a business model id
    status : str = "active"

class PersonaCreate(PersonaBase):
    pass

class PersonaResponse(PersonaBase):
    id : str
    created_at : datetime

class PersonaUpdate(BaseModel):
    name : str | None = None
    job_titles : list[str] | None = None
    industries : list[str] | None = None
    company_size_range : CompanySizeRange | None = None
    lead_source : str | None = None
    model_id : str | None = None 
    status : str | None = None