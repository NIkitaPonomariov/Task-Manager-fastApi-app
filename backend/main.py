from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker, mapped_column
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__="tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan = lifespan)


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
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[TaskSchema] = []


def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id = task_orm.id, title = task_orm.title, completed = task_orm.completed)


@app.get("/tasks")
def tasks_reader(db: Session = Depends(get_db)) -> list[TaskSchema]:
    task_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in task_from_db]


@app.post("/tasks", status_code = status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()
    return task_orm_to_model(task_for_update)

@app.delete("/tasks/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id,  db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()

#!!!!
#create catigories
#end project

# 1.13.37 <- tommorow start from here 

# create models and code for collection 
# end this project , made refactoring 
# puth everything in docker and deploy