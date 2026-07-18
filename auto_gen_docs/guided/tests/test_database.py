"""
Tests for database configuration and dependencies.
"""

from sqlalchemy.orm import Session

from app.database import get_db


def test_get_db_returns_session():
    """
    Test that get_db yields a SQLAlchemy Session.
    """
    db_generator = get_db()

    db = next(db_generator)

    assert isinstance(db, Session)

    # Executes the finally block (db.close())
    db_generator.close()