"""
Database configuration module.

This file is responsible for:
- Creating the SQLite database connection
- Creating SQLAlchemy sessions
- Providing the database base class
- Providing database sessions to FastAPI routes
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file used to store student records
DATABASE_URL = "sqlite:///students.db"


# Creates the connection between SQLAlchemy and the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Creates reusable database sessions
# Each API request receives its own session
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Parent class that all SQLAlchemy models inherit from
Base = declarative_base()

def get_db():
    """
    Creates and provides a database session.

    FastAPI uses this dependency to give routes
    access to the database.

    The session automatically closes after
    the request finishes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()