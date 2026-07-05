from app.models.lead_signal import LeadSignalResponse
from app.models.webhook import WebhookSignalInput
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository
from app.util import convert_to_lead_signal
from app.services.scoring_engine_service import evaluate_signal

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

    signal_id = str(result["_id"])
    await evaluate_signal(signal_id)

    updated_signal = await collection.find_one({"_id" : result["_id"]})
    return convert_to_lead_signal(updated_signal)