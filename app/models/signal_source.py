from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SignalStatus(str,Enum):
    active = "active"
    inactive = "inactive"
    disconnected = "disconnected"

class SignalSourceBase(BaseModel):
    workspace_id : str
    source_name : str
    source_module : str
    status : SignalStatus = SignalStatus.active
    last_event_at : datetime | None = None

class SignalSourceCreate(SignalSourceBase):
    pass

class SignalSourceResponse(SignalSourceBase):
    id : str
    created_at : datetime

class SignalSourceUpdate(BaseModel):
    workspace_id : str | None = None
    source_name : str | None = None
    source_module : str | None = None
    status : SignalStatus | None = None
    last_event_at : datetime | None = None