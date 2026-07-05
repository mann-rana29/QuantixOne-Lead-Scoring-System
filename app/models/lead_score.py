from pydantic import BaseModel
from datetime import datetime
from app.models.score_threshold import BucketName

class LeadScoreBase(BaseModel):
    lead_id : str
    workspace_id : str
    fit_score : int
    engagement_score : int
    negative_score : int
    total_score : int
    bucket : BucketName
    updated_at : datetime

class LeadScoreResponse(LeadScoreBase):
    id : str