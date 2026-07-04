from fastapi import APIRouter
from app.services.lead_service import create, update, delete, find_all, find_by_id
from app.models.lead import LeadCreate, LeadUpdate, LeadResponse

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("/" , response_model=LeadResponse)
async def create_lead(request: LeadCreate):
    return await create(request)

@router.get("/", response_model=list[LeadResponse])
async def find_all_leads():
    return await find_all()

@router.get("/{id}", response_model=LeadResponse)
async def find_lead_by_id(id: str):
    return await find_by_id(id)

@router.put("/{id}", response_model=LeadResponse)
async def update_lead(id : str, request : LeadUpdate):
    return await update(id,request)

@router.delete("/{id}")
async def delete_lead(id : str):
    return await delete(id)