from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from database import get_db, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime

from status_enum import StatusEnum

router = APIRouter(prefix="/task-history", tags=["task-history"])

class TaskHistory(Base):
    __tablename__ = "task_history"
    task_history_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=False)  # Foreign key to Task table
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    timestamp = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task")  # Relationship with Task model

@router.get("/")
def read_task_history(db: Session = Depends(get_db)):
    return db.query(TaskHistory).all()

@router.get("/task/{task_id}")
def get_task_history(task_id: int, db: Session = Depends(get_db)):
    history = db.query(TaskHistory).filter(TaskHistory.task_id == task_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No history found for the given task")
    return history