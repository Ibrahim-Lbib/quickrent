from flask import Flask, render_template
from .config import Config
from .extensions import db, login_manager
from app.models import user, listing
from .routes.auth import auth_bp
from .routes.listings import listing_bp
from .routes.public import public
from .routes.agent import agent_bp

from flask_migrate import Migrate

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(listing_bp)
    app.register_blueprint(public)
    app.register_blueprint(agent_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        db.create_all()
        
    migrate = Migrate(app, db, render_as_batch=False)   
    
    return app