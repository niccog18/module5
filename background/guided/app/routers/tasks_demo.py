# app/routers/tasks_demo.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.utils.notifications import send_email, generate_report

router = APIRouter(prefix="/demo", tags=["Background Tasks Demo"])

class RegistrationRequest(BaseModel):
    name: str
    email: str

@router.post("/register")
def register(request: RegistrationRequest, background_tasks: BackgroundTasks):
    """Register a user and send a welcome email in the background."""
    user_id = 42  # In real code, this comes from the database

    background_tasks.add_task(
        send_email,
        to=request.email,
        subject="Welcome!",
        body=f"Hi {request.name}, welcome to our platform!"
    )

    return {"message": "Registration successful", "user_id": user_id}

@router.post("/report/{user_id}")
def request_report(
    user_id: int,
    report_type: str = "summary",
    background_tasks: BackgroundTasks = None
):
    """Request a report — generation happens in the background."""
    background_tasks.add_task(generate_report, user_id, report_type)

    return {
        "message": f"Report '{report_type}' is being generated",
        "status": "processing",
        "user_id": user_id
    }
