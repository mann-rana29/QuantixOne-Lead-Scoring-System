from app.models.business_model import BusinessModelResponse
from app.models.persona import PersonaResponse
from app.models.score_threshold import ScoreThresholdResponse
from app.models.scoring_rule import ScoringRuleResponse
from app.models.signal_source import SignalSourceResponse
from app.models.lead_signal import LeadSignalResponse
from app.models.lead import LeadResponse

def convert_to_business_model(doc : dict):
    return BusinessModelResponse(
        id= str(doc["_id"]),
        name= doc["name"],
        description= doc.get("description"),
        default_rules= doc.get("default_rules", {}),
        status= doc["status"],
        created_at= doc["created_at"]
    )

def convert_to_persona(doc: dict) -> PersonaResponse:
    return PersonaResponse(
        id=str(doc["_id"]),
        workspace_id=doc["workspace_id"],
        name=doc["name"],
        job_titles=doc.get("job_titles", []),
        industries=doc.get("industries", []),
        company_size_range=doc.get("company_size_range"),
        lead_source=doc.get("lead_source"),
        model_id=doc["model_id"],
        status=doc["status"],
        created_at=doc["created_at"],
    )

def convert_to_score_threshold(doc: dict) -> ScoreThresholdResponse:
    return ScoreThresholdResponse(
        id=str(doc["_id"]),
        workspace_id=doc["workspace_id"],
        bucket_name=doc["bucket_name"],
        from_score=doc["from_score"],
        to_score=doc["to_score"],
        default_action=doc.get("default_action"),
        version_id=doc.get("version_id"),
        created_at=doc["created_at"],
    )

def convert_to_scoring_rule(doc: dict) -> ScoringRuleResponse:
    return ScoringRuleResponse(
        id=str(doc["_id"]),
        workspace_id=doc["workspace_id"],
        name=doc["name"],
        source_module=doc["source_module"],
        trigger_event=doc["trigger_event"],
        condition=doc.get("condition"),
        score_type=doc["score_type"],
        points=doc["points"],
        frequency_limit=doc.get("frequency_limit"),
        apply_to=doc.get("apply_to"),
        status=doc["status"],
        created_at=doc["created_at"],
    )

def convert_to_signal_source(doc : dict) -> SignalSourceResponse:
    return SignalSourceResponse(
        id = str(doc["_id"]),
        workspace_id=doc["workspace_id"],
        source_name=doc["source_name"],
        source_module=doc["source_module"],
        status=doc["status"],
        last_event_at=doc.get("last_event_at"),
        created_at=doc["created_at"]
    )

def convert_to_lead_signal(doc : dict) -> LeadSignalResponse:
    return LeadSignalResponse(
        id = str(doc["_id"]),
        workspace_id=doc["workspace_id"],
        lead_id = doc["lead_id"],
        source = doc["source"],
        event_type=doc["event_type"],
        payload = doc["payload"],
        status=doc["status"],
        processed_at=doc.get("processed_at"),
        created_at = doc["created_at"]
    )

def convert_to_lead(doc : dict) -> LeadResponse:
    return LeadResponse(
        id = str(doc["_id"]),
        workspace_id=doc["workspace_id"],
        name = doc["name"],
        email=doc["email"],
        company=doc["company"],
        job_title=doc["job_title"],
        industry=doc["industry"],
        company_size=doc["company_size"],
        source=doc["source"],
        status= doc["status"],
        created_at=doc["created_at"]
    )