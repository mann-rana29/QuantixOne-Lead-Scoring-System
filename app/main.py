from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connect import connect_to_db, close_db, get_db

@asynccontextmanager
async def lifespan(app : FastAPI):
    await connect_to_db()
    yield
    await close_db()


app = FastAPI(title="Lead Scoring System",lifespan=lifespan)

@app.get("/health")
async def health():
    db = await get_db()
    result = await db.command("ping")

    return {
            "status" : "success",
            "db" : result
            }