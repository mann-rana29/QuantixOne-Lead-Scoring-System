from fastapi import APIRouter
from app.models.lead_signal import LeadSignalCreate, LeadSignalResponse
from app.services.lead_signal_service import create, find_all, find_by_id

router = APIRouter(prefix="/lead-signals",tags=["Lead Signals"])

@router.post("/", response_model=LeadSignalResponse)
async def create_lead_signal(request : LeadSignalCreate):
    return await create(request)

@router.get("/",response_model=list[LeadSignalResponse])
async def find_all_lead_signals():
    return await find_all()

@router.get("/{id}", response_model=LeadSignalResponse)
async def find_lead_signal_by_id(id : str):
    return await find_by_id(id)