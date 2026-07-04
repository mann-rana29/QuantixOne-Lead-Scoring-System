from fastapi import HTTPException
from app.models.lead_signal import LeadSignalCreate
from app.util import convert_to_lead_signal
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository

async def create(request : LeadSignalCreate):
    collection = await get_collection("lead_signals")
    repo = MongoRepository(collection)

    doc = request.model_dump()
    result = await repo.create(doc)

    return convert_to_lead_signal(result)

async def find_all():
    collection = await get_collection("lead_signals")
    repo = MongoRepository(collection)

    docs = await repo.find_all()

    return [convert_to_lead_signal(doc) for doc in docs]

async def find_by_id(id: str):
    collection = await get_collection("lead_signals")
    repo = MongoRepository(collection)

    doc = await repo.find_by_id(id)
    if doc is None:
        raise HTTPException(404, "Lead Signal not found")
    
    return convert_to_lead_signal(doc)
