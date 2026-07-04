from pydantic import BaseModel

class WebhookSignalInput(BaseModel):
    lead_id : str
    source : str
    event_type : str
    payload : dict = {}
