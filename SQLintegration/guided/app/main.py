from fastapi import FastAPI
from app.database import engine, Base
from app.models import task as task_model  # Import so Base registers the model
from app.routers import tasks

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")
app.include_router(tasks.router)
