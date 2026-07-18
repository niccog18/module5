from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    grade_level = Column(Integer)
    gpa = Column(Float)
    is_enrolled = Column(Boolean, default=True)