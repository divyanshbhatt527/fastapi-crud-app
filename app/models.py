# app/models.py
from pydantic import BaseModel, Field
from bson import ObjectId

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: str
    

class ClockIn(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: str
    location: str
