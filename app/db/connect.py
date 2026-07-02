from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = None

async def connect_to_db():
    global client

    DB_URI = os.getenv("MONGO_DB_URI")
    if not DB_URI:
        raise ValueError("DB URI variable is missing!")
    
    client = AsyncIOMotorClient(DB_URI)

    print("MongoDB Atlas is successfully connected.")

async def close_db():
    global client

    if client:
        client.close()
        print("MongoDB Atlas connectin closed!")


async def get_db():
    global client

    DB_NAME= os.getenv("DB_NAME")

    if not DB_NAME:
        raise ValueError("DB_NAME variable is missing!")
    
    if client is None:
        raise RuntimeError("Database client is not initialized!")
    
    return client[DB_NAME]

async def get_collection(name : str):
    db = await get_db()
    return db[name]