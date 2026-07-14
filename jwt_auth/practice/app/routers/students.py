from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.student import Student

from app.schemas.student import (
    StudentCreate,
    StudentResponse,
)

from app.utils.security import get_current_user

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.get(
    "/",
    response_model=list[StudentResponse],
)
def get_students(
    db: Session = Depends(get_db),
):
    return db.query(Student).all()


@router.post(
    "/",
    response_model=StudentResponse,
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    new_student = Student(**student.model_dump())

    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    return new_student


@router.patch("/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    existing = db.get(Student, student_id)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    for key, value in student.model_dump().items():
        setattr(existing, key, value)

    db.commit()

    return existing


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    db.delete(student)

    db.commit()

    return {"message": "Student deleted"}