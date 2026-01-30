"""
config.py uses Pydantic to manage all application seetings. It loads configuration from the environment variables and .env files, with fallback to default values.
This follows the 12-factor app methodology where configuration is separated from code.
"""

#Pydantic is a data validation library and BaseSettings is a special class for managing application settings
#I checked if I had Pydantic by "pip list | findstr pydantic" and I didn't so I installed it by "pip install pydantic-settings" and updated requirements.txt "pip freeze > requirements.txt"
from pydantic_settings import BaseSettings

#Create a Settings class that inherits Pydantic's settings functionality from BaseSettings
#This class will hold all my application configuration
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Falls back to default values if environment variables are not set.
    """
    #Application settings
    app_name: str = "Task Management API"
    app_version: str = "1.0.0"
    debug: bool = True #Debug mode flag - default is true (development mode)

    #Database settings
    #Full connection string to PostgreSQL - postgresql://username:password@host:port/database_name
    database_url: str = "postgresql://task_management_user:password@localhost:5000/task_management_db"

    #Security settings
    secret_key: str = "your-secret-key-change-this-in-production" #Secret key for signing JWT tokens (authentication tokens)
    algorithm: str = "HS256" #Specifies the algorithm for JWT tokens. H (Hash-based Message Authentication Code), S (Secure Hash Algorithm), 256-bit key length
    access_token_expire_minutes: int = 30 #How long login tokens last

    #Special inner class that configures Pydantic's behavior. Tells Pydantic how to load settings
    class Config:
        env_file = ".env" #Tells Pydantic to load settings from a .env file
        case_sensitive = False #Variable names don't have to match case exactly

    #Create a single instance to use throughout the app
    #Loads configuration once at startup and shares the same settings everywhere
    settings = Settings()
