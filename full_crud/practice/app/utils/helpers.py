"""
Helper functions used throughout the API.

Contains reusable logic that does not belong
directly inside CRUD route functions.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.student import Student

def get_student_or_404(
    student_id: int,
    db: Session
) -> Student:
    """
    Retrieves a student by ID.

    Args:
        student_id:
            The student's database ID.

        db:
            Active database session.

    Returns:
        Student object if found.

    Raises:
        HTTP 404 error if the student does not exist.
    """

    student = db.get(
        Student,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student