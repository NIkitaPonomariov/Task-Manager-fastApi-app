from fastapi import APIRouter


router = APIRouter(prefix="/tasks")

@router.get("")
def tasks_reader(db: Session = Depends(get_db)) -> list[TaskSchema]:
    ...

@router.post("", status_code = status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    ...

@router.patch("/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    ...

@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id,  db: Session = Depends(get_db)) -> None:
    ...