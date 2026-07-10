"""
Pydantic schemas for users.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema used to create a user.
    """

    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6
    )


class UserResponse(BaseModel):
    """
    Schema returned to the client.
    """

    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)