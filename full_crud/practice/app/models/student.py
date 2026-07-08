"""
Student database model.

Defines the structure of the students table
inside the SQLite database.
"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Student(Base):
    """
    SQLAlchemy model representing a student.

    Each student contains:
    - Personal information
    - Academic information
    - Enrollment status
    - Account creation timestamp
    """

    __tablename__ = "students"

    # Unique identifier for each student
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Student's full name
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Student email address
    # Must be unique to prevent duplicate accounts
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    # Student grade level (1-12)
    grade_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Optional GPA value
    gpa: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    # Tracks whether the student is currently enrolled
    is_enrolled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # Automatically stores the creation date/time
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )