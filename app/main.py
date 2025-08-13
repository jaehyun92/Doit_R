"""FastAPI application exposing CRUD endpoints for property management.

Endpoints:
- POST   /properties/                 Create a new property
- GET    /properties/                 List all properties
- GET    /properties/{property_id}    Retrieve one property
- PUT    /properties/{property_id}    Update property (partial updates supported)
- DELETE /properties/{property_id}    Delete property

Launch with:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine, Base

# Create database tables on startup if they don't exist yet
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(title="Property Management API", version="1.0.0")


# Dependency for getting a DB session per request
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/properties/", response_model=schemas.PropertyOut, status_code=status.HTTP_201_CREATED)
def create_property(property_in: schemas.PropertyCreate, db: Session = Depends(get_db)) -> schemas.PropertyOut:
    """Create a new property listing and return the created record."""
    db_property = models.Property(
        name=property_in.name,
        address=property_in.address,
        price=property_in.price,
        description=property_in.description,
        owner_name=property_in.owner_name,
        owner_contact=property_in.owner_contact,
        status=(property_in.status.value if hasattr(property_in.status, "value") else property_in.status),
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


@app.get("/properties/", response_model=List[schemas.PropertyOut])
def list_properties(db: Session = Depends(get_db)) -> List[schemas.PropertyOut]:
    """Return all property listings ordered by most recent first."""
    properties = db.query(models.Property).order_by(models.Property.date_listed.desc()).all()
    return properties


@app.get("/properties/{property_id}", response_model=schemas.PropertyOut)
def get_property(property_id: int, db: Session = Depends(get_db)) -> schemas.PropertyOut:
    """Return a single property by its identifier, or 404 if not found."""
    db_property = db.get(models.Property, property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


@app.put("/properties/{property_id}", response_model=schemas.PropertyOut)
def update_property(
    property_id: int, property_update: schemas.PropertyUpdate, db: Session = Depends(get_db)
) -> schemas.PropertyOut:
    """Update fields of an existing property and return the updated record."""
    db_property = db.get(models.Property, property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    update_data = property_update.model_dump(exclude_unset=True)

    # Convert Enum to primitive str for storage
    if "status" in update_data and hasattr(update_data["status"], "value"):
        update_data["status"] = update_data["status"].value

    for field_name, value in update_data.items():
        setattr(db_property, field_name, value)

    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


@app.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a property. Returns 204 on success, 404 if not found."""
    db_property = db.get(models.Property, property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(db_property)
    db.commit()
    return None