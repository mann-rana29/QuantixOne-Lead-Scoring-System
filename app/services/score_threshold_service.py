from app.util import convert_to_score_threshold
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository
from fastapi import HTTPException
from app.models.score_threshold import ScoreThresholdUpdate , ScoreThresholdResponse, ScoreThresholdCreate

async def create(request : ScoreThresholdCreate):
    collection = await get_collection("score_thresholds")
    repo = MongoRepository(collection)

    doc = request.model_dump()

    result = await repo.create(doc)

    return convert_to_score_threshold(result)

async def find_all():
    collection = await get_collection("score_thresholds")
    repo = MongoRepository(collection)

    docs = await repo.find_all()

    return [convert_to_score_threshold(doc) for doc in docs]

async def find_by_id(id : str):
    collection = await get_collection("score_thresholds")
    repo = MongoRepository(collection)

    doc = await repo.find_by_id(id)
    if doc is None:
        raise HTTPException(404, "Score Threshold not found")
    
    return convert_to_score_threshold(doc)

async def update(id : str, request : ScoreThresholdUpdate):
    collection = await get_collection("score_thresholds")
    repo = MongoRepository(collection)

    updated_data = request.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(400, "No detail provided to update")
    
    doc = await repo.update(id, updated_data)
    if doc is None:
        raise HTTPException(404, "Score Threshold not found")
    
    return convert_to_score_threshold(doc)

async def delete(id : str):
    collection = await get_collection("score_thresholds")
    repo = MongoRepository(collection)

    deleted = await repo.delete(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Score Threshold not found")
    
    return {"message": "Score Threshold deleted successfully"}