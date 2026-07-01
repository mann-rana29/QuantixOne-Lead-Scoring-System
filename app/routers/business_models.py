from fastapi import APIRouter
from app.models.business_model import BusinessModelCreate , BusinessModelResponse, BusinessModelUpdate
from app.services.business_model_service import create_business_model, find_all_business_model, find_business_model_by_id, update_business_model, delete_business_model

router = APIRouter(prefix="/business-models", tags=["Business Models"])

@router.post("/",response_model=BusinessModelResponse)
async def create(request : BusinessModelCreate):
    return await create_business_model(request)

@router.get("/", response_model=list[BusinessModelResponse])
async def find_all():
    return await find_all_business_model()

@router.get("/{id}", response_model=BusinessModelResponse)
async def find_by_id(id : str):
    return await find_business_model_by_id(id)

@router.put("/{id}", response_model=BusinessModelResponse)
async def update(id : str, request : BusinessModelUpdate):
    return await update_business_model(id,request)

@router.delete("/{id}")
async def delete(id : str):
    return await delete_business_model(id)
    