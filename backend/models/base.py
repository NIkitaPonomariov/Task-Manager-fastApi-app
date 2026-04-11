from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#base class with id 

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))