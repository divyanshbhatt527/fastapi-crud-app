import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")
client = AsyncIOMotorClient(MONGODB_URI)
database = client[DATABASE_NAME]

def serialize_mongo(item):
    item["id"] = str(item["_id"])
    del item["_id"]
    return item
