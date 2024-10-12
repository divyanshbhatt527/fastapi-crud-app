# app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: str  # Format YYYY-MM-DD

class ItemResponse(ItemCreate):
    id: str
    insert_date: str

class ClockInCreate(BaseModel):
    email: str
    location: str

class ClockInResponse(ClockInCreate):
    id: str
    insert_date: str

class FilterItems(BaseModel):
    email: str = None
    expiry_date: str = None
    insert_date: str = None
    quantity: int = None
