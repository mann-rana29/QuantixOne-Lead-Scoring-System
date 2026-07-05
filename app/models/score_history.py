from pydantic import BaseModel
from datetime import datetime
from app.models.score_threshold import BucketName

class ScoreHistoryBase(BaseModel):
    lead_id : str
    workspace_id : str
    signal_id : str
    rule_id : str
    old_score : int
    score_change : int
    new_score : int
    old_bucket : BucketName
    new_bucket : BucketName
    created_at : datetime

class ScoreHistoryResponse(ScoreHistoryBase):
    id : str