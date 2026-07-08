"""
Student API router.

Contains all CRUD endpoints for students:
- Create student
- Read students
- Update student
- Delete student
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentPatch,
    StudentResponse,
    StudentUpdate,
)
from app.utils.helpers import get_student_or_404


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=201
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Creates a new student.

    Checks whether the email already exists.
    Returns 409 Conflict if duplicate.
    """

    existing = db.scalar(
        select(Student)
        .where(Student.email == student.email)
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    db_student = Student(
        **student.model_dump()
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


@router.get(
    "",
    response_model=list[StudentResponse]
)
def get_students(
    grade_level: int | None = None,
    is_enrolled: bool | None = None,
    db: Session = Depends(get_db)
):
    """
    Returns all students.

    Supports optional filtering by:
    - grade_level
    - enrollment status
    """

    query = select(Student)

    if grade_level is not None:
        query = query.where(
            Student.grade_level == grade_level
        )

    if is_enrolled is not None:
        query = query.where(
            Student.is_enrolled == is_enrolled
        )

    return db.scalars(query).all()


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns a single student by ID.

    Uses helper function to handle 404 errors.
    """

    return get_student_or_404(
        student_id,
        db
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def replace_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    Completely replaces an existing student record.

    PUT requires all fields to be provided.
    """

    db_student = get_student_or_404(
        student_id,
        db
    )

    for key, value in student.model_dump().items():
        setattr(
            db_student,
            key,
            value
        )

    db.commit()
    db.refresh(db_student)

    return db_student


@router.patch(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentPatch,
    db: Session = Depends(get_db)
):
    """
    Partially updates a student.

    Only fields included in the request
    will be modified.
    """

    db_student = get_student_or_404(
        student_id,
        db
    )

    updates = student.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():
        setattr(
            db_student,
            key,
            value
        )

    db.commit()
    db.refresh(db_student)

    return db_student


@router.delete(
    "/{student_id}",
    status_code=204
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Deletes a student record.

    Returns HTTP 204 after successful deletion.
    """

    student = get_student_or_404(
        student_id,
        db
    )

    db.delete(student)
    db.commit()

    return Response(
        status_code=204
    )