from pydantic import BaseModel
from datetime import datetime

class BusinessModelBase(BaseModel):
    name : str
    description: str | None = None
    default_rules : dict = {}
    status : str = "active"

class BusinessModelCreate(BusinessModelBase):
    pass

class BusinessModelResponse(BusinessModelBase):
    id : str
    created_at : datetime

class BusinessModelUpdate(BaseModel):
    name : str | None = None
    description: str | None = None
    default_rules : dict | None = None
    status : str | None = None