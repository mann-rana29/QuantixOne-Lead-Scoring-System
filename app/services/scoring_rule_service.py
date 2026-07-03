from fastapi import HTTPException
from app.models.scoring_rule import ScoringRuleUpdate,ScoringRuleCreate,ScoringRuleResponse
from app.util import convert_to_scoring_rule
from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository

async def create(request : ScoringRuleCreate):
    collection = await get_collection("scoring_rules")
    repo = MongoRepository(collection)

    doc = request.model_dump()
    result = await repo.create(doc)

    return convert_to_scoring_rule(result)

async def find_all():
    collection = await get_collection("scoring_rules")
    repo = MongoRepository(collection)

    docs = await repo.find_all()

    return [convert_to_scoring_rule(doc) for doc in docs]

async def find_by_id(id : str):
    collection = await get_collection("scoring_rules")
    repo = MongoRepository(collection)

    doc = await repo.find_by_id(id)
    if doc is None:
        raise HTTPException(404, "Scoring Rule not found")

    return convert_to_scoring_rule(doc)

async def update(id : str, request : ScoringRuleUpdate):
    collection = await get_collection("scoring_rules")
    repo = MongoRepository(collection)

    updated_data = request.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(400, "No detail provided")
    
    doc = await repo.update(id,updated_data)
    if doc is None:
        raise HTTPException(404, "Scoring Rule not found")
    
    return convert_to_scoring_rule(doc)

async def delete(id : str):
    collection = await get_collection("scoring_rules")
    repo = MongoRepository(collection)

    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(404,"Scoring Rule not found")
    
    return {"message" : "Scoring rule deleted successfully"}