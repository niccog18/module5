from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task in the database."""
    db_task = Task(
        title=task.title,
        description=task.description
    )
    db.add(db_task)           # Stage the new record
    db.commit()               # Save to database
    db.refresh(db_task)       # Reload to get the auto-generated id and created_at
    return db_task            # Pydantic converts via from_attributes

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List tasks with optional completed filter and pagination."""
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
