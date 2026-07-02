from app.models.persona import PersonaResponse, PersonaUpdate, PersonaCreate
from fastapi import APIRouter
from app.services.persona_service import find_all, find_by_id, create, delete, update

router = APIRouter(prefix="/personas", tags=["Personas"])

@router.post("/" , response_model=PersonaResponse)
async def create_persona(request: PersonaCreate):
    return await create(request)

@router.get("/", response_model=list[PersonaResponse])
async def find_all_personas():
    return await find_all()

@router.get("/{id}", response_model=PersonaResponse)
async def find_persona_by_id(id: str):
    return await find_by_id(id)

@router.put("/{id}", response_model=PersonaResponse)
async def update_persona(id : str, request : PersonaUpdate):
    return await update(id,request)

@router.delete("/{id}")
async def delete_persona(id : str):
    return await delete(id)