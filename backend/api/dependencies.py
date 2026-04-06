from backend.services.task import TaskService
from sqlalchemy import Session
from backend.db.session import get_db
from fastapi import Depends

def get_task_servises(db: Session = Depends(get_db)):
    return TaskService(db)