from app.models.business_model import BusinessModelResponse
from app.models.persona import PersonaResponse
from app.models.score_threshold import ScoreThresholdResponse

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