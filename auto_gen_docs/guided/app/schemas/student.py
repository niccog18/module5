from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Student's full name.",
        examples=["Jane Doe"],
    )
    email: str = Field(
        max_length=255,
        description="Student's email address.",
        examples=["jane.doe@example.com"],
    )
    grade_level: int = Field(
        ge=1,
        le=12,
        description="Student's current grade level.",
        examples=[10],
    )
    gpa: float = Field(
        ge=0.0,
        le=4.0,
        description="Student's grade point average.",
        examples=[3.85],
    )
    is_enrolled: bool = Field(
        default=True,
        description="Whether the student is currently enrolled.",
        examples=[True],
    )


class StudentResponse(StudentCreate):
    id: int = Field(
        description="Unique ID assigned to the student.",
        examples=[1],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "grade_level": 10,
                "gpa": 3.85,
                "is_enrolled": True,
            }
        },
    )