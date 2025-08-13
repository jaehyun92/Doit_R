# Property Management API (FastAPI + SQLite)

Simple backend API to manage real estate properties for sale.

## Tech Stack
- Python
- FastAPI
- SQLite (via SQLAlchemy)
- Pydantic v2 for validation

## Setup

1. (Optional) Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the API server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Open API docs (interactive)
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database
- SQLite database file path: `/workspace/properties.db`
- Tables are created automatically on first run.

## Data Model
- Property
  - id (int, PK)
  - name (str)
  - address (str)
  - price (float)
  - description (text)
  - owner_name (str)
  - owner_contact (str)
  - status ("For Sale" | "Under Contract" | "Sold")
  - date_listed (datetime, defaults to now)

## Example Requests

Create a property
```bash
curl -X POST "http://localhost:8000/properties/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "3-bedroom apartment in Gangnam",
    "address": "123 Teheran-ro, Gangnam-gu, Seoul",
    "price": 825000.0,
    "description": "High floor, great view",
    "owner_name": "Jane Doe",
    "owner_contact": "jane@example.com",
    "status": "For Sale"
  }'
```

List all properties
```bash
curl "http://localhost:8000/properties/"
```

Get a single property
```bash
curl "http://localhost:8000/properties/1"
```

Update a property (partial update via PUT)
```bash
curl -X PUT "http://localhost:8000/properties/1" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 799999.0,
    "status": "Under Contract"
  }'
```

Delete a property
```bash
curl -X DELETE "http://localhost:8000/properties/1"
```

## Notes
- The `PUT /properties/{id}` endpoint supports partial updates for convenience.
- Input is validated with Pydantic; invalid requests return 422 with details.
