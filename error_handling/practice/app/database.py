"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


def get_db():
    """
    Creates a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()