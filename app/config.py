import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    """SQLALCHEMY_DATABASE_URI = "postgresql://postgres:E@x3v*g8fM%ndEV@db.yshwjifylvelerylwthi.supabase.co:5432/postgres"
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///quickrent.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
