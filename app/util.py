from app.models.business_model import BusinessModelResponse
from app.models.persona import PersonaResponse

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