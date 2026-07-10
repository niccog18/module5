from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routers.students import router as student_router
from app.utils.exceptions import AppException

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student API")


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = [
        {
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"]
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "detail": "Validation failed",
            "errors": errors
        }
    )


app.include_router(student_router)