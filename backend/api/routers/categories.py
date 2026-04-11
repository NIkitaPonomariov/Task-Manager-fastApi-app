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


@router.post("", status_code = status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_services)
    ) -> CategorySchema:

    return category_service.create_category(payload)


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryService = Depends(get_category_services)
    ) -> CategorySchema:
    try: 
        return category_service.update_category(category_id=category_id, category_update=payload)
    except CategoryNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Category not found")


@router.delete("/{category_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_services)
    ) -> None:
    try:
        return category_service.delete_category(category_id=category_id)
    except CategoryNotFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Category not found")

