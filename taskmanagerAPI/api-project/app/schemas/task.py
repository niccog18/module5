"""Pydantic schemas for task operations."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.enums import Priority


class TaskCreate(BaseModel):
    """Schema for creating tasks."""

    title: str = Field(
        min_length=1,
        max_length=200,
        examples=["Finish Module 5 Project"],
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        examples=["Complete all rubric requirements."],
    )

    priority: Priority = Priority.MEDIUM

    completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for updating tasks."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
    )

    priority: Optional[Priority] = None

    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Returned task information."""

    id: int

    title: str

    description: Optional[str]

    priority: Priority

    completed: bool

    user_id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 5,
                "title": "Finish FastAPI Project",
                "description": "Complete all endpoints.",
                "priority": "high",
                "completed": False,
                "user_id": 1,
                "created_at": "2026-07-22T12:00:00Z",
                "updated_at": "2026-07-22T12:30:00Z",
            }
        },
    )

class SuggestionResponse(BaseModel):
    task_id: int
    task_title: str
    suggestion: str
    ai_ready: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "task_id": 1,
                "task_title": "Finish project",
                "suggestion": "Break this task into smaller steps.",
                "ai_ready": True,
            }
        },
    )

class SuggestionRequest(BaseModel):
    description: str = Field(
        min_length=1,
        max_length=2000,
        examples=[
            "How can I complete this faster?"
        ],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "How can I complete this faster?"
            }
        }
    )