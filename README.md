# Task Manager 

<hr>

## TO-DO
1. Add apis like new user addition, get all tasks, get all users, etc behind admin login.
2. Add Unit Tests
3. Add text based search to get tasks based on description.
4. Integrate with AI to recommend next steps for selected tasks based on description.
5. Integrate the whole BE with FE 
6. FIX docker-compose for app run.

## Development Instructions
1. Run `docker-compose up` (error fastapi_container will be shown, this will be fixed later).
2. Run `python -m uvicorn main:app --reload`, ensure nothing is running on 8000 before this.
3. Open `localhost:8000/docs`, you will get to see all APIs, for protected APIs access, generate access token using login endpoint.



