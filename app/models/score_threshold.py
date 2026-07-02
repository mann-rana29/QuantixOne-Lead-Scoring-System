from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class BucketName(str,Enum):
    cold = "Cold"
    nurture = "Nurture"
    warm = "Warm"
    hot = "Hot"
    sql = "SQL"

class ScoreThresholdBase(BaseModel):
    workspace_id : str
    bucket_name : BucketName
    from_score : int
    to_score : int
    default_action : str | None = None
    version_id : str | None = None

class ScoreThresholdCreate(ScoreThresholdBase):
    pass

class ScoreThresholdResponse(ScoreThresholdBase):
    id : str
    created_at : datetime

class ScoreThresholdUpdate(BaseModel):
    workspace_id : str | None = None
    bucket_name : BucketName | None = None
    from_score : int | None = None
    to_score : int | None = None
    default_action : str | None = None
    version_id : str | None = None