from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks,
    Request,
    status,
    Response,
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse
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
    summary="Retrieve all students",
    responses={
        200: {
            "description": "Successfully retrieved student list"
        },
        429: {
            "description": "Rate limit exceeded"
        },
    },
)
@limiter.limit("60/minute")
def get_students(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Retrieve all students.

    This public endpoint returns a list of all
    student records stored in the database.
    """
    return db.query(Student).all()


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Retrieve a student by ID",
    responses={
        404: {
            "description": "Student not found"
        },
        429: {
            "description": "Rate limit exceeded"
        },
    },
)
@limiter.limit("60/minute")
def get_student(
    request: Request,
    student_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single student by ID.

    Errors:
    - 404: Student does not exist.
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
    summary="Create a new student",
    responses={
        401: {
            "description": "Not authenticated. JWT token required."
        },
        409: {
            "description": "Email already exists"
        },
        422: {
            "description": "Validation error"
        },
        429: {
            "description": "Rate limit exceeded"
        },
    },
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
    Create a new student record.

    Requires authentication.

    The student information is validated using Pydantic
    before being stored in the database.

    Background tasks:
    - Log student creation activity
    - Send a simulated notification

    Errors:
    - 401: Missing or invalid JWT token.
    - 409: Student email already exists.
    - 422: Invalid input data.
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
    summary="Replace a student record",
    responses={
        401: {
            "description": "Not authenticated"
        },
        404: {
            "description": "Student not found"
        },
        422: {
            "description": "Validation error"
        },
    },
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
    Replace all fields for an existing student.

    Requires authentication.

    Errors:
    - 404: Student does not exist.
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


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student record",
    responses={
        401: {
            "description": "Not authenticated"
        },
        404: {
            "description": "Student not found"
        },
        422: {
            "description": "Validation error"
        },
    },
)
@limiter.limit("20/minute")
def update_student(
    request: Request,
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update an existing student record.

    Requires authentication.

    Errors:
    - 404: Student does not exist.
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


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student record",
    responses={
        204: {
            "description": "Student successfully deleted"
        },
        401: {
            "description": "Not authenticated"
        },
        404: {
            "description": "Student not found"
        },
    },
)
@limiter.limit("20/minute")
def delete_student(
    request: Request,
    student_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a student record.

    Requires authentication.

    Background tasks:
    - Log deletion activity

    Errors:
    - 404: Student does not exist.
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