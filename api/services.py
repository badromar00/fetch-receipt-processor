import math
from datetime import datetime, time
from .models import Receipt

def calculate_points(receipt: Receipt) -> int:
    points = 0
    
    # One point for every alphanumeric character in the retailer name
    alphanumeric_count = sum(c.isalnum() for c in receipt.retailer)
    points += alphanumeric_count
    
    # 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith(".00"):
        points += 50
    
    # 25 points if the total is a multiple of 0.25
    total_as_float = float(receipt.total)
    if total_as_float % 0.25 == 0:
        points += 25
    
    # 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5
    
    # If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    for item in receipt.items:
        trimmed_description = item.shortDescription.strip()
        if len(trimmed_description) % 3 == 0:
            item_points = math.ceil(float(item.price) * 0.2)
            points += item_points
    
    # 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d').date()
    if purchase_date.day % 2 == 1:  # Check if day is odd
        points += 6
    
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M').time()
    if time(14, 0) < purchase_time < time(16, 0):
        points += 10
    
    return points 