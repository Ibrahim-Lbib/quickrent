import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///quickrent.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
