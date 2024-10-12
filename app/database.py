from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

client = AsyncIOMotorClient("mongodb://localhost:27017")  
database = client['fastapi_db']

def serialize_mongo(item):
    item["id"] = str(item["_id"])
    del item["_id"]
    return item
