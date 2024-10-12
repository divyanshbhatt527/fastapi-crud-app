# app/routers/clock_in.py
from fastapi import APIRouter, HTTPException
from app.schemas import ClockInCreate, ClockInResponse
from app.database import database, serialize_mongo
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/clock-in", response_model=ClockInResponse)
async def create_clock_in(clock_in: ClockInCreate):
    clock_in_data = clock_in.model_dump()  # Replaces deprecated .dict()
    clock_in_data["insert_date"] = datetime.utcnow().isoformat()

    try:
        result = await database.clock_in.insert_one(clock_in_data)
        clock_in_data["id"] = str(result.inserted_id)
        return clock_in_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating clock-in: {e}")

@router.get("/clock-in/{clock_in_id}", response_model=ClockInResponse)
async def get_clock_in(clock_in_id: str):
    if not ObjectId.is_valid(clock_in_id):
        raise HTTPException(status_code=400, detail="Invalid clock-in ID format")

    record = await database.clock_in.find_one({"_id": ObjectId(clock_in_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return serialize_mongo(record)

@router.delete("/clock-in/{clock_in_id}")
async def delete_clock_in(clock_in_id: str):
    if not ObjectId.is_valid(clock_in_id):
        raise HTTPException(status_code=400, detail="Invalid clock-in ID format")

    result = await database.clock_in.delete_one({"_id": ObjectId(clock_in_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return {"detail": "Clock-in record deleted successfully"}

@router.put("/clock-in/{clock_in_id}", response_model=ClockInResponse)
async def update_clock_in(clock_in_id: str, clock_in: ClockInCreate):
    if not ObjectId.is_valid(clock_in_id):
        raise HTTPException(status_code=400, detail="Invalid clock-in ID format")

    update_data = clock_in.model_dump()

    result = await database.clock_in.update_one({"_id": ObjectId(clock_in_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Clock-in record not found")

    updated_record = await database.clock_in.find_one({"_id": ObjectId(clock_in_id)})
    return serialize_mongo(updated_record)

@router.get("/clock-in/filter/", response_model=list[dict])
async def filter_clock_ins(email: str = None, location: str = None, insert_date: str = None):
    filters = {}
    print('Entered filter_clock_ins')
    if email:
        filters["email"] = email

    if location:
        filters["location"] = location

    if insert_date:
        try:
            filters["insert_date"] = {"$gt": datetime.fromisoformat(insert_date)}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

    clock_ins = await database.clock_in.find(filters).to_list(100)
    
    if not clock_ins:
        raise HTTPException(status_code=404, detail="No clock-in records found")

    return [serialize_mongo(record) for record in clock_ins]