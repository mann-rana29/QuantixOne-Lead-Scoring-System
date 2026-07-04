import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

WORKSPACE_ID = "test-workspace-1"

async def seed():
    client = AsyncIOMotorClient(os.getenv("MONGO_DB_URI"))
    db = client[os.getenv("DB_NAME")]

    # Clear existing test data first
    for coll in ["business_models", "personas", "scoring_rules",
                 "score_thresholds", "leads", "lead_signals"]:
        await db[coll].delete_many({"workspace_id": WORKSPACE_ID})

    now = datetime.utcnow()

    # 1. Business Model
    bm_result = await db["business_models"].insert_one({
        "name": "B2B Sales",
        "description": "Standard B2B lead scoring model",
        "default_rules": {},
        "status": "active",
        "created_at": now,
    })
    business_model_id = str(bm_result.inserted_id)

    # 2. Persona
    await db["personas"].insert_one({
        "workspace_id": WORKSPACE_ID,
        "name": "Enterprise Buyer",
        "job_titles": ["VP Sales", "Head of Growth", "CRO"],
        "industries": ["SaaS", "Fintech"],
        "company_size_range": {"min": 50, "max": 1000},
        "lead_source": "organic",
        "model_id": business_model_id,
        "status": "active",
        "created_at": now,
    })

    # 3. Scoring Rules
    rules = [
        {
            "workspace_id": WORKSPACE_ID,
            "name": "Business Email Present",
            "source_module": "contacts",
            "trigger_event": "email_captured",
            "condition": None,
            "score_type": "Fit",
            "points": 10,
            "frequency_limit": 1,
            "apply_to": "once_ever",
            "status": "active",
            "created_at": now,
        },
        {
            "workspace_id": WORKSPACE_ID,
            "name": "Pricing Page Visited",
            "source_module": "js_tracker",
            "trigger_event": "page_view",
            "condition": {"field": "page", "operator": "equals", "value": "/pricing"},
            "score_type": "Engagement",
            "points": 20,
            "frequency_limit": 1,
            "apply_to": "per_day",
            "status": "active",
            "created_at": now,
        },
        {
            "workspace_id": WORKSPACE_ID,
            "name": "Email Bounced",
            "source_module": "mail",
            "trigger_event": "email_bounced",
            "condition": None,
            "score_type": "Negative",
            "points": 20,
            "frequency_limit": None,
            "apply_to": None,
            "status": "active",
            "created_at": now,
        },
        {
            "workspace_id": WORKSPACE_ID,
            "name": "WhatsApp Replied",
            "source_module": "whatsapp",
            "trigger_event": "message_replied",
            "condition": None,
            "score_type": "Engagement",
            "points": 15,
            "frequency_limit": 3,
            "apply_to": "per_day",
            "status": "active",
            "created_at": now,
        },
    ]
    await db["scoring_rules"].insert_many(rules)

    # 4. Score Thresholds (all 5 buckets)
    thresholds = [
        {"workspace_id": WORKSPACE_ID, "bucket_name": "Cold", "from_score": 0, "to_score": 19, "default_action": "none", "version_id": None, "created_at": now},
        {"workspace_id": WORKSPACE_ID, "bucket_name": "Nurture", "from_score": 20, "to_score": 39, "default_action": "add_to_nurture", "version_id": None, "created_at": now},
        {"workspace_id": WORKSPACE_ID, "bucket_name": "Warm", "from_score": 40, "to_score": 69, "default_action": "notify_manager", "version_id": None, "created_at": now},
        {"workspace_id": WORKSPACE_ID, "bucket_name": "Hot", "from_score": 70, "to_score": 89, "default_action": "trigger_routing", "version_id": None, "created_at": now},
        {"workspace_id": WORKSPACE_ID, "bucket_name": "SQL", "from_score": 90, "to_score": 100, "default_action": "trigger_routing", "version_id": None, "created_at": now},
    ]
    await db["score_thresholds"].insert_many(thresholds)

    # 5. Leads
    lead_result = await db["leads"].insert_one({
        "workspace_id": WORKSPACE_ID,
        "name": "Test Lead One",
        "email": "test.lead@examplecorp.com",
        "company": "Example Corp",
        "job_title": "VP Sales",
        "industry": "SaaS",
        "company_size": 200,
        "source": "webform",
        "status": "active",
        "created_at": now,
    })
    lead_id = str(lead_result.inserted_id)

    print("Seed complete.")
    print(f"workspace_id: {WORKSPACE_ID}")
    print(f"business_model_id: {business_model_id}")
    print(f"lead_id: {lead_id}")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed())