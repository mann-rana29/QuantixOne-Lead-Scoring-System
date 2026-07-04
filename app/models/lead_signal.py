from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class LeadSignalStatus(str, Enum):
    pending = "pending"
    processed = "processed"
    failed = "failed"

class LeadSignalBase(BaseModel):
    workspace_id : str
    lead_id : str
    source : str
    event_type : str
    payload : dict
    status : LeadSignalStatus = LeadSignalStatus.pending
    processed_at : datetime | None = None

class LeadSignalResponse(LeadSignalBase):
    id : str
    created_at : datetime

class LeadSignalCreate(LeadSignalBase):
    pass