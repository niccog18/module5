from pydantic import BaseModel, ConfigDict, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    is_enrolled: bool = True


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    is_enrolled: bool | None = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_enrolled: bool

    model_config = ConfigDict(from_attributes=True)