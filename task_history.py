from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from database import get_db, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from task import Task

router = APIRouter(prefix="/task-history", tags=["task-history"])

class TaskHistory(Base):
    __tablename__ = "task_history"
    task_history_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=False)  # Foreign key to Task table
    status_change = Column(String(100), nullable=False)  # Example: "Pending to Completed"
    timestamp = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task")  # Relationship with Task model

@router.get("/")
def read_task_history(db: Session = Depends(get_db)):
    return db.query(TaskHistory).all()

@router.post("/add")
def add_task_history(task_id: int, status_change: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_history = TaskHistory(task_id=task_id, status_change=status_change)
    db.add(new_history)
    db.commit()
    return new_history

@router.get("/task/{task_id}")
def get_task_history(task_id: int, db: Session = Depends(get_db)):
    history = db.query(TaskHistory).filter(TaskHistory.task_id == task_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No history found for the given task")
    return history