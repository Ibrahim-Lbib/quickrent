import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///rentals.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
