from app.models.business_model import BusinessModelResponse, BusinessModelCreate, BusinessModelUpdate
from app.db.connect import get_db
from datetime import datetime
from app.util import convert_to_business_model
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

async def create_business_model(request : BusinessModelCreate) -> BusinessModelResponse:
    db = await get_db()
    collection = db["business_models"]
    
    doc = request.model_dump()
    doc["created_at"] = datetime.utcnow()

    result = await collection.insert_one(doc)
    created = await collection.find_one({"_id": result.inserted_id})

    return convert_to_business_model(created)

async def find_all_business_model() -> list[BusinessModelResponse]:
    db = await get_db()
    collection = db["business_models"]

    cursor = collection.find()

    result = []
    async for doc in cursor:
        result.append(convert_to_business_model(doc))

    return result

async def find_business_model_by_id(id):
    db = await get_db()
    collection = db["business_models"]
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400,detail="Invalid Id format")
    
    query_filter = {"_id" : object_id}

    doc = await collection.find_one(query_filter)
    if doc is None:
        raise HTTPException(404, "Business Model not found")
    
    return convert_to_business_model(doc)

async def update_business_model(id : str, request : BusinessModelUpdate):
    db = await get_db()
    collection = db["business_models"]

    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(400, "Invalid Id format")
    
    update_data = request.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(400, "No detail provided to update")
    
    result = await collection.update_one({"_id" : object_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(404, "Business Model not found")
    
    doc = await collection.find_one({"_id" : object_id})

    return convert_to_business_model(doc)

async def delete_business_model(id : str):
    db = await get_db()
    collection = db["business_models"]

    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(400, "Invalid Id format")
    
    result = await collection.delete_one({"_id" : object_id})

    if result.deleted_count == 0:
        raise HTTPException(404, "Business Model not found")
    
    return {"message" : "Business model deleted successfully"}