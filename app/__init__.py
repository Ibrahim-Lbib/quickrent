from flask import Flask, render_template
import os
from .config import config_by_name
from .extensions import db, login_manager
from .routes.auth import auth_bp
from .routes.public import public
from .routes.agent import agent_bp
from .routes.payments import payments

from flask_migrate import Migrate

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "dev")
        
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_by_name[config_name])

    @app.template_filter("intcomma")
    def intcomma(value):
        """Format integers with comma separators (e.g. 800000 -> 800,000)."""
        try:
            return f"{int(value):,}"
        except (TypeError, ValueError):
            return value

    @app.template_filter("ugx")
    def ugx(value):
        """Format UGX integers with comma separators (e.g. 800000 -> 'UGX 800,000')."""
        try:
            return f"UGX {int(value):,}"
        except (TypeError, ValueError):
            return value

    @app.template_filter("ugx_short")
    def ugx_short(value):
        """Format UGX values in shorthand (e.g. 800000 -> 'UGX 800K', 1200000 -> 'UGX 1.2M')."""
        try:
            amount = int(value)
        except (TypeError, ValueError):
            return value

        if amount >= 1_000_000:
            m = amount / 1_000_000
            text = f"{m:.1f}".rstrip("0").rstrip(".")
            return f"UGX {text}M"
        if amount >= 1_000:
            return f"UGX {amount // 1_000}K"
        return f"UGX {amount}"
    
    db.init_app(app)
    login_manager.init_app(app)
    # We'll show more specific messaging on the login page based on `next=...`.
    login_manager.login_message = None
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(public)
    app.register_blueprint(agent_bp)
    app.register_blueprint(payments)
    
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
