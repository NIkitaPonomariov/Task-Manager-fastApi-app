from fastapi import APIRouter, status, Depends, HTTPException
from backend.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from backend.services.category import CategoryService, CategoryNotFound
from backend.api.dependencies import get_category_services

router = APIRouter(prefix="/categories")

@router.get("/")
def category_reader(
    category_service: CategoryService = Depends(get_category_services)
) -> list[CategorySchema]:
    return category_service.get_categories()

"""

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



"""