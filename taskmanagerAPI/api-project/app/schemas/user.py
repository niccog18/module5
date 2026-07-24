"""Pydantic schemas for user authentication and responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""

    name: str = Field(
        min_length=2,
        max_length=100,
        examples=["Jane Doe"],
    )

    email: EmailStr = Field(
        examples=["jane@example.com"],
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["SecurePassword123"],
    )


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(
        examples=["jane@example.com"],
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["SecurePassword123"],
    )


class UserResponse(BaseModel):
    """Returned user information."""

    id: int

    name: str

    email: EmailStr

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Jane Doe",
                "email": "jane@example.com",
                "is_active": True,
                "created_at": "2026-07-22T12:00:00Z",
            }
        },
    )


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str

    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer",
            }
        }
    )
