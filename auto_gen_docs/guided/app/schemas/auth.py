from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        description="Unique username for the new account.",
        examples=["nicco123"],
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password containing at least 8 characters.",
        examples=["SecurePass123!"],
    )


class LoginRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        description="Registered username.",
        examples=["nicco123"],
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password associated with the account.",
        examples=["SecurePass123!"],
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        description="JWT access token used for authenticated requests.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        description="Type of authentication token.",
        examples=["bearer"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    }