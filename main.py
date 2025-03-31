from fastapi import FastAPI
from database import engine, Base
from users import router as user_router
 
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(user_router)
