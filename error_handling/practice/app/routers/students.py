from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
)
from app.utils.exceptions import (
    BadRequestException,
    DuplicateException,
    NotFoundException,
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    db_student = Student(**student.model_dump())

    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

    except IntegrityError:
        db.rollback()

        raise DuplicateException(
            "Student",
            "email",
            student.email
        )

    return db_student


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise NotFoundException(
            "Student",
            student_id
        )

    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    updates: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise NotFoundException(
            "Student",
            student_id
        )

    for key, value in updates.model_dump(
        exclude_unset=True
    ).items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError:
        db.rollback()

        raise DuplicateException(
            "Student",
            "email",
            updates.email
        )

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise NotFoundException(
            "Student",
            student_id
        )

    if student.is_enrolled:
        raise BadRequestException(
            "Cannot delete an enrolled student."
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully."
    }