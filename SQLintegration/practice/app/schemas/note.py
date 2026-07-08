from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str
    category: str | None = None
    is_pinned: bool = False


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str | None
    is_pinned: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)