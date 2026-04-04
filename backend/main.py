from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker 

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
    new_task = TaskSchema(id=str(uuid4()), title=payload.title,completed=False)

    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskUpdateSchema:
    for task in tasks:
        if task.id == task_id:
            task.title = payload.title if payload.title else task.title
            task.completed = payload.completed if payload.completed is not None else task.completed
            return task
        

@app.delete("/tasks/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


#!!!!
#create catigories
#end project

# 1.13.37 <- tommorow start from here 

# create models and code for collection 
# end this project , made refactoring 
# puth everything in docker and deploy