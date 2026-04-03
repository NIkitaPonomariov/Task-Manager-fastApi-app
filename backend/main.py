from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:3000"],
    allow_methods = ["*"]
)


class TaskSchema(BaseModel):
    id: str
    tittle: str
    complete: bool

class TaskCreateSchema(BaseModel):
    tittle: str

tasks: list[TaskSchema] = []


@app.get("/tasks")
def tasks_reader() -> list[TaskSchema]:
    return tasks


@app.post("/tasksadd")
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), tittle=payload.tittle,complete=False)

    tasks.append(new_task)
    return new_task

