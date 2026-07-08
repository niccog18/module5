"""
Pydantic schemas for Student API validation.

Schemas define:
- What data users can send
- What data the API returns
- Validation rules for incoming requests
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class StudentCreate(BaseModel):
    """
    Schema used when creating a new student.

    Requires the information needed to create
    a student database record.
    """

    name: str
    email: str
    grade_level: int = Field(
        ge=1,
        le=12
    )
    gpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=4
    )
    is_enrolled: bool = True


class StudentUpdate(BaseModel):
    """
    Schema used for PUT requests.

    PUT replaces the entire resource,
    therefore all fields are required.
    """

    name: str
    email: str
    grade_level: int = Field(
        ge=1,
        le=12
    )
    gpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=4
    )
    is_enrolled: bool


class StudentPatch(BaseModel):
    """
    Schema used for PATCH requests.

    Allows updating only the fields
    provided by the user.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    grade_level: Optional[int] = Field(
        default=None,
        ge=1,
        le=12
    )
    gpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=4
    )
    is_enrolled: Optional[bool] = None


class StudentResponse(BaseModel):
    """
    Schema returned by the API.

    Includes database-generated fields
    such as id and created_at.
    """

    id: int
    name: str
    email: str
    grade_level: int
    gpa: Optional[float]
    is_enrolled: bool
    created_at: datetime

    # Allows Pydantic to convert SQLAlchemy objects
    # into API responses
    model_config = ConfigDict(
        from_attributes=True
    )