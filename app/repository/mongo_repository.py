from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

class MongoRepository:
    def __init__(self, collection):
        self.collection = collection

    async def create(self,data:dict) -> dict:
        result = await self.collection.insert_one(data)
        return await self.collection.find_one({"_id" : result.inserted_id})
    
    async def find_all(self) -> list[dict]:
        return [doc async for doc in self.collection.find()]
    
    async def find_by_id(self, id: str) -> dict | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid id format")
        return await self.collection.find_one({"_id": object_id})

    async def update(self, id: str, data: dict) -> dict | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid id format")
        
        result = await self.collection.update_one({"_id": object_id}, {"$set": data})
        if result.matched_count == 0:
            return None
        
        return await self.collection.find_one({"_id": object_id})

    async def delete(self, id: str) -> bool:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid id format")
        
        result = await self.collection.delete_one({"_id": object_id})
        return result.deleted_count > 0