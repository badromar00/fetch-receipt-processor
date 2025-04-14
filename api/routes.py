from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid

from .models import Receipt, ReceiptResponse, PointsResponse
from .services import calculate_points

router = APIRouter()

# In-memory storage for receipts and their points using dictionaries
receipt_store: Dict[str, dict] = {}
points_store: Dict[str, int] = {}

@router.post("/receipts/process", response_model=ReceiptResponse)
async def process_receipt(receipt: Receipt):
    # Generate a unique ID
    receipt_id = str(uuid.uuid4())
    
    # Store the receipt
    receipt_store[receipt_id] = receipt.dict()
    
    # Calculate and store points
    points = calculate_points(receipt)
    points_store[receipt_id] = points
    
    return {"id": receipt_id}

@router.get("/receipts/{id}/points", response_model=PointsResponse)
async def get_points(id: str):
    if id not in points_store:
        raise HTTPException(status_code=404, detail="No receipt found for that ID")
    
    return {"points": points_store[id]} 