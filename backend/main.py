from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskSchema(BaseModel):
    id: str
    title: str
    complete: bool

class TaskCreateSchema(BaseModel):
    title: str

tasks: list[TaskSchema] = []


@app.get("/tasks")
def tasks_reader() -> list[TaskSchema]:
    return tasks


@app.post("/tasks")
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title,complete=False)

    tasks.append(new_task)
    return new_task

