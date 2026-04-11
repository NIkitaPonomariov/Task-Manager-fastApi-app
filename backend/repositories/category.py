from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()
    
    def get_category_by_id(self, category_id) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)
    
    def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, category: CategoryORM) -> None:
        self.db.delete(CategoryORM)