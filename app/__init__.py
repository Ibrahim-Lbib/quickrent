from flask import Flask, render_template, request, redirect, url_for
from .config import Config
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('home.html')
    
    
    return app