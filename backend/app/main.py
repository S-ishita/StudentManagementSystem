from fastapi import FastAPI
from .routes import router as student_router

app = FastAPI()

app.include_router(student_router, tags=["Student"], prefix="/students")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Student Management System"}
