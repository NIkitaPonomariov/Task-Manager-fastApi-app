from sqlalchemy.orm import Session
from backend.repositories.category import CategoryRepository
from backend.schemas.category import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)

class CategoryNotFound(Exception):
    """Category not found"""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_categories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()
        return [
            CategorySchema.model_validate(category)
            for category in categories_orm
        ]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repository.create(
            name=category_create.name
        )
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(
        self,
        category_id: str,
        category_update: CategoryUpdateSchema,
    ) -> CategorySchema:
        category = self.category_repository.get_by_id(category_id)

        if not category:
            raise CategoryNotFound(f"category with id={category_id} not found")

        if category_update.name:
            category.name = category_update.name

        self.db.commit()
        return CategorySchema.model_validate(category)

    def delete_category(self, category_id: str) -> None:
        category = self.category_repository.get_by_id(category_id)

        if not category:
            raise CategoryNotFound(f"category with id={category_id} not found")

        self.category_repository.delete(category)
        self.db.commit()