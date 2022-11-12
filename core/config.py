import os
from pathlib import Path
from datetime import timedelta

class BaseConfig:
    BASE_DIR = Path(__file__).resolve().parent
    SECRET_KEY = "TheSecretKey"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER  = os.path.join(BASE_DIR, 'media')
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    
    # JSON Web Token Configuration
    JWT_SECRET_KEY = "The JWT Secret Key"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_COOKIE_SECURE = True
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

class DevelopmentConfig(BaseConfig):
    pass