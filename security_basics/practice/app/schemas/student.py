from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )
    email: str = Field(
        max_length=255
    )
    grade_level: int = Field(
        ge=1,
        le=12
    )
    gpa: float = Field(
        ge=0.0,
        le=4.0
    )
    is_enrolled: bool = True


class StudentResponse(StudentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)