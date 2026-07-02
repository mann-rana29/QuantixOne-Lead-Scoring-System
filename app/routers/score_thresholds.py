from fastapi import APIRouter
from app.models.score_threshold import ScoreThresholdResponse , ScoreThresholdUpdate, ScoreThresholdCreate
from app.services.score_threshold_service import create, update, find_by_id, find_all, delete

router = APIRouter(prefix="/score-thresholds",tags=["Score Thresholds"])

@router.post("/", response_model=ScoreThresholdResponse)
async def create_score_threshold(request : ScoreThresholdCreate):
    return await create(request)

@router.get("/", response_model=list[ScoreThresholdResponse])
async def find_all_score_threshold():
    return await find_all()

@router.get("/{id}", response_model=ScoreThresholdResponse)
async def find_score_threshold_by_id(id : str):
    return await find_by_id(id)

@router.put("/{id}", response_model=ScoreThresholdResponse)
async def update_score_threshold( id : str, request : ScoreThresholdUpdate):
    return await update(id,request)

@router.delete("/{id}")
async def delete_score_threshold(id : str):
    return await delete(id)