# Fetch Receipt Processor

## Language Choice
I chose Python with FastAPI for this assignment because:
- A framework I have been recently learning, and enjoying
- FastAPI provides excellent automatic API documentation and validation
- Python's string manipulation and datetime handling are well-suited for the points calculation rules
- The framework's automatic OpenAPI (Swagger) documentation makes it easy to test and understand the API

## Docker Setup
The application is containerized using Docker and requires no additional configuration to run. To run the application:

1. Clone the repository:
```bash
git clone https://github.com/badromar00/fetch-receipt-processor.git
cd fetch-receipt-processor
```

2. Build and run the Docker container:
```bash
docker build -t receipt-processor .
docker run -p 8000:8000 receipt-processor
```

The API will be available at `http://localhost:8000`

The Dockerfile:
- Uses Python 3.9 slim image for a minimal footprint
- Copies all necessary files
- Installs dependencies from requirements.txt
- Exposes port 8000
- Runs the FastAPI application using uvicorn

## Features

- Process receipts and calculate points based on some rules using RESTful API endpoints
- Input validation for receipt data
- Interactive API documentation (Swagger UI and ReDoc) automatically made when using FastAPI

## Points Calculation Rules

1. One point for every alphanumeric character in the retailer name
2. 50 points if the total is a round dollar amount with no cents
3. 25 points if the total is a multiple of 0.25
4. 5 points for every two items on the receipt
5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer
6. 6 points if the day in the purchase date is odd
7. 10 points if the time of purchase is after 2:00pm and before 4:00pm

## API Endpoints

### Process Receipt
- **POST** `/receipts/process`
- Accepts a JSON receipt and returns a unique ID
- Request body example:
```json
{
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        },
        {
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
        },
        {
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
        },
        {
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
        },
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
        }
    ],
    "total": "35.35"
}
```
- Response example:
```json
{
    "id": "6bfdfdfb-9c2b-4ca5-a3e7-6335478f8e7d"
}
```

### Get Points
- **GET** `/receipts/{id}/points`
- Returns the points calculated for a specific receipt
- Response example:
```json
{
    "points": 28
}
```

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing the API

### Process a Receipt
```bash
curl -X POST "http://localhost:8000/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
         "retailer": "Target",
         "purchaseDate": "2022-01-01",
         "purchaseTime": "13:01",
         "items": [
             {
                 "shortDescription": "Mountain Dew 12PK",
                 "price": "6.49"
             },
             {
                 "shortDescription": "Emils Cheese Pizza",
                 "price": "12.25"
             },
             {
                 "shortDescription": "Knorr Creamy Chicken",
                 "price": "1.26"
             },
             {
                 "shortDescription": "Doritos Nacho Cheese",
                 "price": "3.35"
             },
             {
                 "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                 "price": "12.00"
             }
         ],
         "total": "35.35"
     }'
```
### Get Points
```bash
curl "http://localhost:8000/receipts/{id}/points"
```
Replace `{id}` with the ID returned from the process endpoint.
## Error Handling

The API includes validation for all input fields and returns appropriate error messages:

- Invalid date format: Must be YYYY-MM-DD
- Invalid time format: Must be HH:MM (24-hour)
- Invalid price format: Must be XX.XX
- Invalid retailer name: Only alphanumeric characters, spaces, hyphens, and ampersands allowed
- Invalid item description: Only alphanumeric characters, spaces, and hyphens allowed

Example error response:
```json
{
    "detail": "Date must be in format YYYY-MM-DD"
}
```
