from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import get_db, Base
from sqlalchemy import Column, Integer, String
from auth import create_access_token, auth_required

router = APIRouter(prefix="/users", tags=["users"])

class LoginRequest(BaseModel):
    email: str
    password: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token.
    """
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    # Verify password
    if not check_password_hash(user.password, request.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


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
def update_user(id: int, name: str, email: str, password: str = None, db: Session = Depends(get_db), payload: dict = Depends(auth_required)):
    if not is_same_user(payload, id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")
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
def delete_user(
        id: int,
        payload: dict = Depends(auth_required),
        db: Session = Depends(get_db)
):
    if not is_same_user(payload, id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def is_same_user(payload, user_id, db):
    user_email = payload.get("sub")
    if not user_email:
        return False
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return False
    return user.id == user_id
