from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, relationship

from auth import auth_required
from database.database import get_db, Base
from sqlalchemy import Column, Integer, String, ForeignKey

from api.users import is_same_user

router = APIRouter(prefix="/categories", tags=["categories"])

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name =  Column(String(100), unique=True, nullable=False)
    category_description = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to User table

    user = relationship("User")  # Establish relationship with User model

@router.get("/")
def read_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/add")
async def add_category(request: Request, category_name: str = None, category_description: str = None, user_id: int = None, db: Session = Depends(get_db), payload: dict = Depends(auth_required) ):
    if user_id is None:
        req_body = await request.json()
        user_id = int(req_body.get("userId"))
        category_name = req_body.get("categoryName")
        category_description = req_body.get("category_description")

    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")
    category = db.query(Category).filter(Category.category_name == category_name).first()
    if category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(category_name=category_name, category_description=category_description, user_id=user_id)
    db.add(new_category)
    db.commit()
    return new_category

@router.put("/update/{id}")
def update_category(category_id: int, category_name: str, category_description: str = None, user_id: int = None, db: Session = Depends(get_db), payload: dict = Depends(auth_required)):
    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.category_name = category_name
    category.category_description= category_description
    if user_id is not None: 
        category.user_id = user_id
    db.commit()
    return category

@router.delete("/delete/{id}")
def delete_category(category_id: int, user_id: int =None, db: Session = Depends(get_db), payload: dict = Depends(auth_required)):
    if not is_same_user(payload, user_id, db):
        raise HTTPException(status_code=403, detail="You are not authorized to update this task")
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}