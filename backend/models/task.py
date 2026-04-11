from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

#class with task(id we have in base class)

class TaskORM(Base):
    __tablename__="tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)