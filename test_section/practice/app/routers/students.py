from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks, 
    Request, 
    status, 
    Response
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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

from app.utils.limiter import limiter

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.get(
    "/",
    response_model=list[StudentResponse],
)
@limiter.limit("60/minute")
def get_students(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Public endpoint.
    """
    return db.query(Student).all()


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
@limiter.limit("60/minute")
def get_student(
    request: Request,
    student_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single student by ID.
    """

    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
def create_student(
    request: Request,
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
    try:
        db.commit()
        db.refresh(new_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

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

@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
@limiter.limit("20/minute")
def replace_student(
    request: Request,
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Replace a student record.
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


@router.patch("/{student_id}")
@limiter.limit("20/minute")
def update_student(
    request: Request,
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
@limiter.limit("20/minute")
def delete_student(
    request: Request,
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

    return Response(status_code=204)