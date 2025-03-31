from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from database import get_db, Base
from sqlalchemy import Column, Integer, String

router = APIRouter(prefix="/users", tags=["users"])

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/add")
def add_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return new_user

@router.put("/update/{id}")
def update_user(id: int, name: str, email: str, password: str = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.email = email
    if password:
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
    db.commit()
    return user

@router.delete("/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
