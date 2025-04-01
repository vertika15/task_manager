from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, Base
from sqlalchemy import Column, Integer, String
from auth import create_access_token, auth_required

router = APIRouter(prefix="/users", tags=["users"])

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token.
    """
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    # Verify password
    if not check_password_hash(user.password, password):
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
def delete_user(
        id: int,
        payload: dict = Depends(auth_required),  # Enforces JWT authentication and extracts user payload
        db: Session = Depends(get_db)
):
    """
    Allows only an authenticated user to delete their own account.

    Args:
        id (int): The user ID to delete.
        payload (dict): Data extracted from the decoded JWT (e.g., user's email).
        db (Session): SQLAlchemy database session.
    """
    # Extract user email from the decoded token
    user_email = payload.get("sub")  # Extracting the "sub" (subject) field from the token
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token or user not authenticated")

    # Fetch the user with this ID from the database
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure the authenticated user can only delete their own account
    if user.email != user_email:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")

    # Proceed to delete the user
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
