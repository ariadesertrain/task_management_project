#This file defines the entry point for the web application
#This also defines what URLs the API responds to

#IMPORTING LIBRARIES
#Import FastAPI library
from fastapi import FastAPI
#Import Middleware library
from fastapi.middleware.cors import CORSMiddleware

#Create an instance of the FastAPI
app = FastAPI(
    title = "Task Management API",
    description = "JIRA Replacement",
    version = "1.0.0"
)

#Configure CORS (Cross-Origin Resource Sharing)
#This allows our React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["HTTP://localhost:5000"], #React dev server
    allow_credentials = True,
    allow_methods = ["*"], #Allow all HTTP methods (GET(retrieve data),POST(create new data),PUT(update data),DELETE,etc.)
    allow_headers = ["*"] #Allow all headers
)

#Root endpoint - just to test if the server is running
@app.get("/")
def homepage():
    return {
        "message":"Welcome to Task Management",
        "status":"Running",
        "docs":"/docs"
    }

#Health check endpoint - useful for monitoring
@app.get("/healthcheck")
def healthcheck():
    return{
        "status":"Healthy"
    }