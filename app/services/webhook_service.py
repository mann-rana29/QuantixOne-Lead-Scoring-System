from app.models.lead_signal import LeadSignalResponse
from app.models.webhook import WebhookSignalInput
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository
from app.util import convert_to_lead_signal
async def ingest_signal(workspace_id : str, request: WebhookSignalInput):
    collection = await get_collection("lead_signals")
    repo = MongoRepository(collection)

    doc = {
        "workspace_id" : workspace_id,
        "lead_id": request.lead_id,
        "source": request.source,
        "event_type": request.event_type,
        "payload": request.payload,
        "status": "pending",
        "processed_at": None,
    }

    result = await repo.create(doc)
    return convert_to_lead_signal(result)