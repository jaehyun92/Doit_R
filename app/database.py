"""Database setup for the Property Management API.

- Creates a SQLAlchemy engine connected to a SQLite database
- Exposes a session factory for request-scoped sessions
- Defines the declarative base used by ORM models
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Absolute path to the SQLite database file for consistency in this environment
SQLALCHEMY_DATABASE_URL = "sqlite:////workspace/properties.db"

# For SQLite, `check_same_thread` must be False when using the connection across threads (FastAPI workers)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory; each request will get its own session via dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative ORM models
Base = declarative_base()