from http.client import HTTPException

from fastapi import APIRouter, status, Depends
from backend.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from backend.services.task import TaskService, TaskNotFound
from backend.api.dependencies import get_task_servises

router = APIRouter(prefix="/categories")


#here i write all for categories!!!

