from fastapi import HTTPException
from app.models.lead import LeadCreate, LeadUpdate, LeadResponse
from app.util import convert_to_lead
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository

async def create(request : LeadCreate):
    collection = await get_collection("leads")
    repo = MongoRepository(collection)

    doc = request.model_dump()
    result = await repo.create(doc)

    return convert_to_lead(result)

async def find_all():
    collection = await get_collection("leads")
    repo = MongoRepository(collection)

    docs = await repo.find_all()
    
    return [convert_to_lead(doc) for doc in docs]

async def find_by_id(id : str):
    collection = await get_collection("leads")
    repo = MongoRepository(collection)

    doc = await repo.find_by_id(id)
    if doc is None:
        raise HTTPException(404, "Lead not found")
    
    return convert_to_lead(doc)

async def update(id : str, request : LeadUpdate):
    collection = await get_collection("leads")
    repo = MongoRepository(collection)

    updated_data = request.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(400, "No data to update")
    
    doc = await repo.update(id,updated_data)
    if doc is None:
        raise HTTPException(404, "Lead not found")
    
    return convert_to_lead(doc)

async def delete(id: str):
    collection = await get_collection("leads")
    repo = MongoRepository(collection)

    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(404, "Lead not found")
    
    return {"message" : "Lead deleted successfully"}
