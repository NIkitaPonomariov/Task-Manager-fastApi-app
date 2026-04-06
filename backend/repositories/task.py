from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.task import TaskORM


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[TaskORM]:
        return self.db.scalars(select(TaskORM)).all()
    
    def get_task_by_id(self, task_id) -> TaskORM:
        return self.db.get(TaskORM, task_id)
    
    def create_task(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        self.db.commit()

    def delete(self, TaskORM) -> None:
        self.db.delete(TaskORM)