from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(
        description="Unique user ID",
        examples=[1],
    )

    username: str = Field(
        description="Account username",
        examples=["nicco123"],
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "nicco123",
            }
        },
    }