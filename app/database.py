import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URI)
database = client.get_default_database()

def serialize_mongo(item):
    item["id"] = str(item["_id"])
    del item["_id"]
    return item
