"""SQLAlchemy ORM models.

Defines the `Property` table schema.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime

from .database import Base


class Property(Base):
    """Represents a real estate property listed for sale."""

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    owner_name = Column(String(255), nullable=False)
    owner_contact = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="For Sale")
    date_listed = Column(DateTime, nullable=False, default=datetime.utcnow)