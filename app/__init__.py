from flask import Flask, render_template, Blueprint, request, redirect, url_for
from .config import Config
from .extensions import db, login_manager
from app.models import user, listing, category, location
from .routes.auth import auth_bp
from .routes.listings import listing_bp
from .routes.public import public

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(public)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        db.create_all()
    @app.route('/')
    def index():
        return render_template('home.html')    
    
    return app