import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
<<<<<<< HEAD
    """SQLALCHEMY_DATABASE_URI = "postgresql://postgres:E@x3v*g8fM%ndEV@db.yshwjifylvelerylwthi.supabase.co:5432/postgres"
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///quickrent.db"
=======
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///quickrent.db")
>>>>>>> 9bb1097fae2b760f199fee584003653ea525eb9d
    SQLALCHEMY_TRACK_MODIFICATIONS = False
