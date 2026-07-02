from app.models.business_model import BusinessModelResponse, BusinessModelCreate, BusinessModelUpdate
from app.db.connect import get_collection
from app.util import convert_to_business_model
from fastapi import HTTPException
from app.repository.mongo_repository import MongoRepository

async def create_business_model(request : BusinessModelCreate) -> BusinessModelResponse:
    collection = await get_collection("business_models")
    
    doc = request.model_dump()

    repo = MongoRepository(collection)

    created = await repo.create(doc)

    return convert_to_business_model(created)

async def find_all_business_model() -> list[BusinessModelResponse]:
    collection = await get_collection("business_models")

    repo = MongoRepository(collection)

    docs = await repo.find_all()
    return [convert_to_business_model(doc) for doc in docs]

async def find_business_model_by_id(id):
    collection = await get_collection("business_models")

    repo = MongoRepository(collection)
    doc = await repo.find_by_id(id)
    
    if doc is None:
        raise HTTPException(status_code=404, detail="Business model not found")
    return convert_to_business_model(doc)

async def update_business_model(id : str, request : BusinessModelUpdate):
    collection = await get_collection("business_models")

    repo = MongoRepository(collection)
    
    update_data = request.model_dump(exclude_unset=True)
    if update_data is None:
        raise HTTPException(400, "No detail provided to update")
    
    doc = await repo.update(id,update_data)
    
    if doc is None:
        raise HTTPException(status_code=404, detail="Business model not found")
    return convert_to_business_model(doc)

async def delete_business_model(id : str):
    collection = await get_collection("business_models")

    repo = MongoRepository(collection)
    deleted = await repo.delete(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Business model not found")
    
    return {"message": "Business model deleted successfully"}