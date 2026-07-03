from fastapi import APIRouter
from app.models.signal_source import SignalSourceUpdate , SignalSourceResponse, SignalSourceCreate
from app.services.signal_source_service import create, update, find_all, find_by_id, delete

router = APIRouter(prefix="/signal-sources", tags=["Signal Sources"])

@router.post("/", response_model=SignalSourceResponse)
async def create_signal_source(request : SignalSourceCreate):
    return await create(request)

@router.get("/", response_model=list[SignalSourceResponse])
async def find_all_signal_sources():
    return await find_all()

@router.get("/{id}", response_model=SignalSourceResponse)
async def find_signal_source_by_id(id : str):
    return await find_by_id(id)

@router.put("/{id}", response_model=SignalSourceResponse)
async def update_signal_source(id : str,request : SignalSourceUpdate):
    return await update(id,request)

@router.delete("/{id}")
async def delete_signal_source(id: str):
    return await delete(id)