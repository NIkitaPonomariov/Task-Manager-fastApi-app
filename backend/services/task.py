from sqlalchemy.orm import Session
from backend.repositories.task import TaskRepository
from backend.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema 

class TaskNotFound(Exception):
    """task not found"""

class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository()

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repository.create(title = task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)
    
    def update_task(self,task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        try:
            task_for_update = self.task_repository.get_task_by_id(task_id=task_id)
        except Exception:
            raise TaskNotFound("task with id={task_id} not found")
        if task_for_update.title:
            task_for_update.title = task_for_update.title
        if task_for_update.completed is not None:
            task_for_update.completed = task_for_update.completed

        self.db.commit()
        return TaskSchema.model_validate(task_for_update)


    def delete_task(self,task_id: str) -> None:
        try:
            task_for_delete = self.task_repository.get_task_by_id(task_id=task_id)
        except Exception:
            raise TaskNotFound(f"task with id={task_id} not found")
        self.task_repository.delete(task_for_delete)