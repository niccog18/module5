"""Task management endpoints."""

from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.enums import Priority
from app.exceptions import (
    NotFoundException,
    ForbiddenException,
)
from app.models.task import Task
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    SuggestionResponse,
    SuggestionRequest,
)

router = APIRouter()


def log_task_activity(action: str, task_id: int) -> None:
    """
    Background task that logs task activity.

    Args:
        action: Action performed on the task.
        task_id: Task identifier.
    """

    with open("task_activity.log", "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now(timezone.utc)} | "
            f"{action} | Task ID: {task_id}\n"
        )


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    The created task is automatically associated
    with the currently logged-in user.
    """

    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=task.completed,
        user_id=current_user.id,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    background_tasks.add_task(
        log_task_activity,
        "Created",
        db_task.id,
    )

    return db_task

@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="List tasks",
)
def list_tasks(
    completed: bool | None = Query(
        default=None,
        description="Filter by completion status.",
    ),
    priority: Priority | None = Query(
        default=None,
        description="Filter by task priority.",
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of tasks to skip.",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of tasks to return.",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    """
    Return tasks belonging to the authenticated user.

    Optional query parameters allow filtering by
    completion status, priority, and pagination.
    """

    query = db.query(Task).filter(
        Task.user_id == current_user.id
    )

    if completed is not None:
        query = query.filter(
            Task.completed == completed
        )

    if priority is not None:
        query = query.filter(
            Task.priority == priority
        )

    tasks = (
        query.order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return tasks

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Retrieve a single task belonging to the authenticated user.

    Raises:
    NotFoundException:
        If the task does not exist.

    ForbiddenException:
        If the task belongs to another user.
    """

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise NotFoundException(
    "Task not found"
)

    if task.user_id != current_user.id:
        raise ForbiddenException(
    "You do not have permission to access this task"
)

    return task

@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Partially update a task belonging to the authenticated user.

    Only fields supplied in the request body are updated.

    Raises:
    NotFoundException:
        If the task does not exist.

    ForbiddenException:
        If the task belongs to another user.
    """

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise NotFoundException(
    "Task not found"
)

    if task.user_id != current_user.id:
        raise ForbiddenException(
    "You do not have permission to update this task"
)

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)

    return task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a task belonging to the authenticated user.

    Raises:
    NotFoundException:
        If the task does not exist.

    ForbiddenException:
        If the task belongs to another user.
    """

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise NotFoundException(
    "Task not found"
)

    if task.user_id != current_user.id:
        raise ForbiddenException(
    "You do not have permission to delete this task"
)

    task_id_deleted = task.id

    db.delete(task)
    db.commit()

    background_tasks.add_task(
        log_task_activity,
        "Deleted",
        task_id_deleted,
    )

    return None

@router.post(
    "/{task_id}/suggest",
    response_model=SuggestionResponse,
    summary="Generate AI task suggestion",
)
def suggest_task_action(
    task_id: int,
    request: SuggestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SuggestionResponse:
    """
    Provide a placeholder AI-generated suggestion
    for a task.

    This endpoint is designed as a future integration
    point for an AI model.

    Raises:
    NotFoundException:
        If the task does not exist.

    ForbiddenException:
        If the task belongs to another user.
    """

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise NotFoundException(
    "Task not found"
)

    if task.user_id != current_user.id:
        raise ForbiddenException(
    "You do not have permission to access this task"
)

    suggestion = (
    f"You asked: '{request.description}'. "
    "AI suggestion: Break this task into smaller, manageable steps."
)

    return {
        "task_id": task.id,
        "task_title": task.title,
        "suggestion": suggestion,
        "ai_ready": True,
    }