from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from database import get_db, Base
from sqlalchemy import Column, Integer, String, ForeignKey

router = APIRouter(prefix="/categories", tags=["categories"])

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), unique=True, nullable=False)
    category_description = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to User table

    user = relationship("User")  # Establish relationship with User model

@router.get("/")
def read_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/add")
def add_category(category_name: str, category_description: str = None, user_id: int = None, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_name == category_name).first()
    if category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(category_name=category_name, category_description=category_description, user_id=user_id)
    db.add(new_category)
    db.commit()
    return new_category

@router.put("/update/{id}")
def update_category(category_id: int, category_name: str, category_description: str = None, user_id: int = None, db: Session = Depends(get_db)):
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
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}