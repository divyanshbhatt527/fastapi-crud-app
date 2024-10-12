from fastapi import APIRouter, HTTPException
from app.schemas import ItemCreate, ItemResponse, FilterItems
from app.database import database, serialize_mongo
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    print("Health check received")
    return {"status": "healthy"}

@router.post("/items/create/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    print('Entered create')
    
    try:
        expiry_date = datetime.strptime(item.expiry_date, "%Y-%m-%d")  
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")
    
    item_data = item.model_dump()  
    item_data["insert_date"] = datetime.now().isoformat() 

    try:
        result = await database.items.insert_one(item_data)  
        item_data["id"] = str(result.inserted_id)
        return item_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")
    
@router.get("/items/get_all/", response_model=list[ItemResponse])
async def get_all_items():
    items = await database.items.find().to_list(100)  
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return [serialize_mongo(item) for item in items]

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID format")

    item = await database.items.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return serialize_mongo(item)

@router.delete("/items/{item_id}/delete")
async def delete_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID format")

    result = await database.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted successfully"}

@router.put("/items/{item_id}/update", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemCreate):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID format")

    update_data = item.model_dump()

    result = await database.items.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = await database.items.find_one({"_id": ObjectId(item_id)})
    return serialize_mongo(updated_item)

@router.get("/items/filter/", response_model=list[ItemResponse])
async def filter_items(
    email: str = None,
    expiry_date: str = None,
    insert_date: str = None,
    quantity: int = None,
):
    filters = {}
    if email:
        filters["email"] = email
    if expiry_date:
        try:
            filters["expiry_date"] = {"$gt": datetime.fromisoformat(expiry_date)}
        except Exception as e:
            print(f'Error occured : {e}')
            raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD)")
    if insert_date:
        try:
            filters["insert_date"] = {"$gt": datetime.fromisoformat(insert_date)}
        except Exception as e:
            print(f'Error occured : {e}')
            raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD)")
    if quantity:
        filters["quantity"] = {"$gte": quantity}

    items = await database.items.find(filters).to_list(100)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return [serialize_mongo(item) for item in items]

@router.get("/items/aggregate/", response_model=list[dict])
async def aggregate_items(min_quantity: int = None):
    pipeline = []

    if min_quantity:
        pipeline.append({"$match": {"quantity": {"$gte": min_quantity}}})

    pipeline.append({
        "$group": {
            "_id": "$email",
            "count": {"$sum": 1}
        }
    })

    result = await database.items.aggregate(pipeline).to_list(None)

    if not result:
        raise HTTPException(status_code=404, detail="No items found")

    return result
