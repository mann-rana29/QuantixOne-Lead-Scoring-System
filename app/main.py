from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connect import connect_to_db, close_db, get_db
from app.routers.business_models import router as business_models_router
from app.routers.personas import router as persona_router
from app.routers.score_thresholds import router as score_threshold_router
from app.routers.scoring_rules import router as scoring_rule_router
from app.routers.signal_sources import router as signal_source_router
from app.routers.lead_signals import router as lead_signal_router
from app.routers.leads import router as lead_router
from app.routers.webhooks import router as webhook_router

@asynccontextmanager
async def lifespan(app : FastAPI):
    await connect_to_db()
    yield
    await close_db()


app = FastAPI(title="Lead Scoring System",lifespan=lifespan)

app.include_router(business_models_router)
app.include_router(persona_router)
app.include_router(score_threshold_router)
app.include_router(scoring_rule_router)
app.include_router(signal_source_router)
app.include_router(lead_signal_router)
app.include_router(lead_router)
app.include_router(webhook_router)

@app.get("/")
async def root():
    return {"message" : "backend is live"}

@app.get("/health")
async def health():
    db = await get_db()
    result = await db.command("ping")

    return {"status" : "success","db" : result}