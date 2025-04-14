from pydantic import BaseModel, validator
from typing import List
import re
from datetime import datetime

class Item(BaseModel):
    shortDescription: str
    price: str
    
    @validator('price')
    def validate_price(cls, v):
        if not re.match(r'^\d+\.\d{2}$', v):
            raise ValueError('Price must be in format XX.XX')
        return v
    
    @validator('shortDescription')
    def validate_short_description(cls, v):
        if not re.match(r'^[\w\s\-]+$', v):
            raise ValueError('Short description contains invalid characters')
        return v

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str  # Format: YYYY-MM-DD
    purchaseTime: str  # Format: HH:MM (24-hour)
    items: List[Item]
    total: str  # Format: XX.XX
    
    @validator('retailer')
    def validate_retailer(cls, v):
        if not re.match(r'^[\w\s\-&]+$', v):
            raise ValueError('Retailer contains invalid characters')
        return v
    
    @validator('purchaseDate')
    def validate_purchase_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in format YYYY-MM-DD')
        return v
    
    @validator('purchaseTime')
    def validate_purchase_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Time must be in format HH:MM (24-hour)')
        return v
    
    @validator('total')
    def validate_total(cls, v):
        if not re.match(r'^\d+\.\d{2}$', v):
            raise ValueError('Total must be in format XX.XX')
        return v

class ReceiptResponse(BaseModel):
    id: str

class PointsResponse(BaseModel):
    points: int 