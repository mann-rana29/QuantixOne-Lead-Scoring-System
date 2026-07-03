from pydantic import BaseModel
from enum import Enum

class ConditionOperator(str,Enum):
    equals = "equals"
    not_equals = "not_equals"
    contains = "contains"
    greater_than = "greater_than"
    less_than = "less_than"

class Condition(BaseModel):
    field : str
    operator : ConditionOperator 
    value : str | int | float

class ScoreType(str,Enum):
    fit = "Fit"
    engagement = "Engagement"
    negative = "Negative"
    decay = "Decay"

class ScoringRuleBase(BaseModel):
    workspace_id : str
    name : str
    source_module : str
    trigger_event : str
    condition : Condition | None = None
    score_type : ScoreType
    points : int
    frequency_limit : int | None = None
    apply_to: str | None = None
    status : str = "active"

class ScoringRuleCreate(ScoringRuleBase):
    pass

class ScoringRuleUpdate(BaseModel):
    workspace_id : str | None = None
    name : str | None = None
    source_module : str | None = None
    trigger_event : str | None = None
    condition : Condition | None = None
    score_type : ScoreType | None = None
    points : int | None = None
    frequency_limit : int | None = None
    apply_to: str | None = None
    status : str | None = None