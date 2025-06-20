from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.api.core import database, models, schemas, jwt


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.TaskOut], summary="List my tasks")
def list_tasks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(jwt.get_current_user),
):
    """List all tasks belonging to the current user."""
    return db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).all()


# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.TaskOut, summary="Create a task")
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(jwt.get_current_user),
):
    """Create a new task for the current user."""
    db_task = models.Task(**task_in.model_dump(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# PUBLIC_INTERFACE
@router.get("/{task_id}", response_model=schemas.TaskOut, summary="Get a task by ID")
def get_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(jwt.get_current_user),
):
    """Fetch a single task by ID (must be owned by user)."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task


# PUBLIC_INTERFACE
@router.put("/{task_id}", response_model=schemas.TaskOut, summary="Update a task")
def update_task(
    task_id: int,
    update: schemas.TaskUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(jwt.get_current_user),
):
    """Update a task (must be owned by user)."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


# PUBLIC_INTERFACE
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(jwt.get_current_user),
):
    """Delete a task (must be owned by user)."""
    task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    db.delete(task)
    db.commit()
    return None
