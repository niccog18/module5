from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.student import Student

from app.schemas.student import (
    StudentCreate,
    StudentResponse,
)

from app.utils.security import get_current_user

from app.utils.notifications import (
    log_activity,
    send_notification,
)

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
    """
    Public endpoint.
    """
    return db.query(Student).all()


@router.post(
    "/",
    response_model=StudentResponse,
)
def create_student(
    student: StudentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a student.

    Background tasks:
    - Log activity
    - Simulate notification
    """

    new_student = Student(**student.model_dump())

    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    background_tasks.add_task(
        log_activity,
        current_user.id,
        f"Created student {new_student.id}",
    )

    background_tasks.add_task(
        send_notification,
        student.email,
        f"Welcome {student.name}! "
        "Your student record has been created.",
    )

    return new_student


@router.patch("/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update a student.
    """

    existing = db.get(Student, student_id)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    for key, value in student.model_dump().items():
        setattr(existing, key, value)

    db.commit()

    db.refresh(existing)

    return existing


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a student.

    Background task:
    - Log activity
    """

    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    db.delete(student)

    db.commit()

    background_tasks.add_task(
        log_activity,
        current_user.id,
        f"Deleted student {student_id}",
    )

    return {
        "message": "Student deleted"
    }