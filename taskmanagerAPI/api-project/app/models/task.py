"""Task database model."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums import Priority


class Task(Base):
    """
    Represents a task owned by a user.
    """

    __tablename__ = "tasks"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )


    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )


    description: Mapped[Optional[str]] = mapped_column(
        String(2000),
        nullable=True,
    )


    priority: Mapped[Priority] = mapped_column(
        Enum(Priority),
        default=Priority.MEDIUM,
        nullable=False,
    )


    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


    user: Mapped["User"] = relationship(
        "User",
        back_populates="tasks",
    )