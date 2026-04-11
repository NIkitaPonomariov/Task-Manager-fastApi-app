from http.client import HTTPException

from fastapi import APIRouter, status, Depends
from backend.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from backend.services.task import TaskService, TaskNotFound
from backend.api.dependencies import get_task_servises

router = APIRouter(prefix="/tasks")

@router.get("")
def tasks_reader(
    task_service: TaskService = Depends(get_task_servises)
    ) -> list[TaskSchema]:

    return task_service.list_tasks()

@router.post("", status_code = status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema,
    task_service: TaskService = Depends(get_task_servises)
    ) -> TaskSchema:

    return task_service.create_task(task_create=payload)

@router.patch("/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_servises)
    ) -> TaskSchema:
    try: 
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_servises)
    ) -> None:
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)


