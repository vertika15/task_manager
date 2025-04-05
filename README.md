# Task Manager 

<hr>

## TO-DO
1. Add apis like new user addition, get all tasks, get all users, etc behind admin login.
2. Add Unit Tests
3. Add text based search to get tasks based on description.
4. Integrate with AI to recommend next steps for selected tasks based on description.
5. FIX docker-compose for app run.
6. Expose get all tasks for a user API
7. Expose available categories API
8. Add JWT token and secret outside code as env config

## Development Instructions
1. Run `docker-compose up` (error fastapi_container will be shown, this will be fixed later).
2. Run `python -m uvicorn main:app --reload`, ensure nothing is running on 8000 before this.
3. [Optional] Open `localhost:8000/docs`, you will get to see all APIs, for protected APIs access, generate access token using login endpoint.
4. Run `python -m http.server 8080 `, this will bring up FE server at 8080. Access `localhost:8080` to access FE.



