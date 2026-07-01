from app.models.business_model import BusinessModelResponse

def convert_to_business_model(doc):
    return BusinessModelResponse(
        id= str(doc["_id"]),
        name= doc["name"],
        description= doc.get("description"),
        default_rules= doc.get("default_rules", {}),
        status= doc["status"],
        created_at= doc["created_at"]
    )