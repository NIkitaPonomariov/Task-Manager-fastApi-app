from backend.services.task import TaskService
from backend.services.category import CategoryService
from sqlalchemy.orm import Session
from backend.db.session import get_db
from fastapi import Depends

def get_task_servises(db: Session = Depends(get_db)):
    return TaskService(db)

def get_category_services(db: Session = Depends(get_db)):
    return CategoryService(db)