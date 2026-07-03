from fastapi import HTTPException
from app.models.signal_source import SignalSourceCreate, SignalSourceResponse, SignalSourceUpdate
from app.util import convert_to_signal_source
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository

async def create(request : SignalSourceCreate):
    collection = await get_collection("signal_sources")
    repo = MongoRepository(collection)

    doc = request.model_dump()
    result = await repo.create(doc)

    return convert_to_signal_source(result)

async def find_all():
    collection = await get_collection("signal_sources")
    repo = MongoRepository(collection)

    docs = await repo.find_all()

    return [convert_to_signal_source(doc) for doc in docs]

async def find_by_id(id : str):
    collection = await get_collection("signal_sources")
    repo = MongoRepository(collection)

    doc = await repo.find_by_id(id)
    if doc is None:
        raise HTTPException(404, "Signal Source not found")
    
    return convert_to_signal_source(doc)

async def update(id : str, request : SignalSourceUpdate):
    collection = await get_collection("signal_sources")
    repo = MongoRepository(collection)

    updated_data = request.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(400, "Update data is missing")
    
    doc = await repo.update(id, updated_data)
    if doc is None:
        raise HTTPException(404, "Signal Source not found")

    return convert_to_signal_source(doc)

async def delete(id : str):
    collection = await get_collection("signal_sources")
    repo = MongoRepository(collection)

    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(404, "Signal Source not found")
    
    return {"message" : "Signal Source deleted successfully"}
