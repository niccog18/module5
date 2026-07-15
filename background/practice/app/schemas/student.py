from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    name: str
    email: str
    grade_level: int
    gpa: float
    is_enrolled: bool = True


class StudentResponse(StudentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)