from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship

from auth import auth_required
from database import get_db, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime

from status_enum import StatusEnum
from task_history import TaskHistory
from users import is_same_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to users table
    task_name = Column(String(200), nullable=False)
    task_description = Column(String(500), nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String(50), nullable=True)  # Example: "Low", "Medium", "High"
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)  # Foreign key to categories table
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")  # Relationship with User model
    category = relationship("Category")  # Relationship with Category model

@router.get("/")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.post("/add")
def add_task(
    task_name: str,
    task_description: str = None,
    due_date: datetime = None,
    priority: str = None,
    status: StatusEnum = StatusEnum.PENDING,
    user_id: int = None,
    category_id: int = None,
    payload: dict = Depends(auth_required),
    db: Session = Depends(get_db),
):
    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")
    new_task = Task(
        task_name=task_name,
        task_description=task_description,
        due_date=due_date,
        priority=priority,
        status=status,
        user_id=user_id,
        category_id=category_id,
    )
    db.add(new_task)
    db.commit()
    return new_task

@router.put("/update/{id}")
def update_task(
        task_id: int,
        task_name: str = None,
        task_description: str = None,
        due_date: datetime = None,
        priority: str = None,
        status: StatusEnum = None,
        user_id: int = None,
        category_id: int = None,
        payload: dict = Depends(auth_required),
        db: Session = Depends(get_db),
):
    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")

    # Fetch the task to be updated
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")

    # Update the task fields if they are provided in the request
    if task_name:
        task.task_name = task_name
    if task_description:
        task.task_description = task_description
    if due_date:
        task.due_date = due_date
    if priority:
        task.priority = priority
    if status is not None:
        task.status = status
    if user_id:
        task.user_id = user_id
    if category_id:
        task.category_id = category_id

    db.commit()
    return task


@router.delete("/delete/{id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: int = None, payload: dict = Depends(auth_required)):
    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.get("/execute/{task_id}")
def execute_task(task_id: int, db: Session = Depends(get_db), user_id: int = None, payload: dict = Depends(auth_required)):
    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_history = TaskHistory(task_id=task_id, status=StatusEnum.COMPLETED.value)
    db.add(new_history)
    return {"message":"Task executed successfully", "task": new_history}

