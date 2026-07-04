from fastapi import APIRouter
from app.models.webhook import WebhookSignalInput
from app.models.lead_signal import LeadSignalResponse
from app.services.webhook_service import ingest_signal

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/{workspace_id}/signals", response_model=LeadSignalResponse)
async def receive_webhook_signal(workspace_id : str, request : WebhookSignalInput):
    return await ingest_signal(workspace_id,request)