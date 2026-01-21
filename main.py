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

#Add the Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["HTTP://localhost:5000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#Create a new endpoint
@app.get("/")
def homepage():
    return {
        "message":"Welcome to Task Management",
        "status":"Running",
        "docs":"/docs"
    }

#Create a health check endpoint
@app.get("/healthcheck")
def healthcheck():
    return{
        "status":"Healthy"
    }