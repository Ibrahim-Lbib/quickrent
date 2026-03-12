from flask import Flask, render_template
import os
from .config import config_by_name
from .extensions import db, login_manager
from .routes.auth import auth_bp
from .routes.public import public
from .routes.agent import agent_bp

from flask_migrate import Migrate

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "dev")
        
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_by_name[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(public)
    app.register_blueprint(agent_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    
    # db.create_all() removed - use flask-migrate for schema changes
        
    Migrate(app, db, render_as_batch=(config_name == 'dev'))   
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404
    
    return app
