from fastapi import FastAPI
from database.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware as CM

from api.users import router as user_router
from api.task import router as task_router
from api.task_history import router as task_history_router
from api.categories import router as categories_router
 
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CM,
    allow_origins=["*"],  # Temporarily allow all origins during testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(user_router)
app.include_router(task_router)
app.include_router(task_history_router)
app.include_router(categories_router)
