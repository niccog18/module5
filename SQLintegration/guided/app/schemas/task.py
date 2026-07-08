from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: Optional[datetime]    # datetime, not str - SQLAlchemy returns a datetime object

    model_config = ConfigDict(from_attributes=True)    # Read from SQLAlchemy model objects
    