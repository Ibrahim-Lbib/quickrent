from flask import Flask, render_template, Blueprint, request, redirect, url_for
from .config import Config
from .extensions import db, login_manager
from .routes.auth import auth_bp
from .routes.listings import listing_bp

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.register_blueprint(auth_bp)
    app.register_blueprint(listing_bp)
    
    @app.route('/')
    def index():
        return render_template('home.html')    
    
    return app