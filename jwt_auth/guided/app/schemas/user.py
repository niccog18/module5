from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
