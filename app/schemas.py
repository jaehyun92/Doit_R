"""Pydantic models for API request/response validation.

Includes enums and data schemas for properties.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PropertyStatus(str, Enum):
    """Enumeration of valid property listing statuses."""

    for_sale = "For Sale"
    under_contract = "Under Contract"
    sold = "Sold"


class PropertyBase(BaseModel):
    """Shared attributes for creating and reading properties."""

    name: str = Field(..., min_length=1, max_length=255, examples=["3-bedroom apartment in Gangnam"])
    address: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., ge=0, description="Listing price; must be non-negative")
    description: Optional[str] = Field(None, max_length=5000)
    owner_name: str = Field(..., min_length=1, max_length=255)
    owner_contact: str = Field(..., min_length=1, max_length=255)
    status: PropertyStatus = Field(default=PropertyStatus.for_sale)


class PropertyCreate(PropertyBase):
    """Payload to create a new property."""

    pass


class PropertyUpdate(BaseModel):
    """Payload to update an existing property. All fields are optional for partial updates."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=5000)
    owner_name: Optional[str] = Field(None, min_length=1, max_length=255)
    owner_contact: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[PropertyStatus] = None


class PropertyOut(PropertyBase):
    """Response schema representing a property as returned by the API."""

    id: int
    date_listed: datetime

    # Enable reading data directly from ORM objects
    model_config = ConfigDict(from_attributes=True)