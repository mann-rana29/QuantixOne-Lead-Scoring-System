from app.db.connect import get_collection
from app.repository.mongo_repository import MongoRepository
from app.util import convert_to_persona
from app.models.persona import PersonaResponse, PersonaUpdate, PersonaCreate
from fastapi import HTTPException

async def create(request : PersonaCreate):
    collection = await get_collection("personas")
    repo = MongoRepository(collection)

    doc = request.model_dump()

    result = await repo.create(doc)

    return convert_to_persona(result)

async def find_all():
    collection = await get_collection("personas")
    repo = MongoRepository(collection)

    docs = await repo.find_all()

    return [convert_to_persona(doc) for doc in docs]

async def find_by_id(id: str):
    collection = await get_collection("personas")
    repo = MongoRepository(collection)

    doc = await repo.find_by_id(id)
    if doc is None:
        raise HTTPException(404, "Pesona not found")

    return convert_to_persona(doc)

async def update(id: str, request : PersonaUpdate):
    collection = await get_collection("personas")
    repo = MongoRepository(collection)

    update_data = request.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(400, "No detail provided to update")
    
    doc = await repo.update(id,update_data)
    if doc is None:
        raise HTTPException(404, "Persona not found")
    
    return convert_to_persona(doc)

async def delete(id : str):
    collection = await get_collection("personas")
    repo = MongoRepository(collection)

    deleted = await repo.delete(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    return {"message": "Persona deleted successfully"}