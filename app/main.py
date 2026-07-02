from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connect import connect_to_db, close_db, get_db
from app.routers.business_models import router as business_models_router
from app.routers.personas import router as persona_router

@asynccontextmanager
async def lifespan(app : FastAPI):
    await connect_to_db()
    yield
    await close_db()


app = FastAPI(title="Lead Scoring System",lifespan=lifespan)

app.include_router(business_models_router)
app.include_router(persona_router)

@app.get("/health")
async def health():
    db = await get_db()
    result = await db.command("ping")

    return {"status" : "success","db" : result}