from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

client = AsyncIOMotorClient("mongodb+srv://divyanshbhatt527:kwyb7UEdg2mUDRcS@cluster0.3u2wv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  
database = client['fastapi_db']

def serialize_mongo(item):
    item["id"] = str(item["_id"])
    del item["_id"]
    return item
