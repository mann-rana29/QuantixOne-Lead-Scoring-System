from fastapi import APIRouter
from app.models.scoring_rule import ScoringRuleUpdate , ScoringRuleCreate , ScoringRuleResponse
from app.services.scoring_rule_service import create, update, find_all, find_by_id, delete

router = APIRouter(prefix="/scoring-rules", tags=["Scoring Rules"])

@router.post("/", response_model=ScoringRuleResponse)
async def create_scoring_rule(request : ScoringRuleCreate):
    return await create(request)

@router.get("/", response_model=list[ScoringRuleResponse])
async def find_all_scoring_rules():
    return await find_all()

@router.get("/{id}", response_model=ScoringRuleResponse)
async def find_scoring_rule_by_id(id : str):
    return await find_by_id(id)

@router.put("/{id}", response_model=ScoringRuleResponse)
async def update_scoring_rule(id : str,request : ScoringRuleUpdate):
    return await update(id,request)

@router.delete("/{id}")
async def delete_scoring_rule(id: str):
    return await delete(id)

