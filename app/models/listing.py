# rooms, apartments, shops
from app.extensions import db

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    price = db.Column(db.Integer, nullable=False)
    
    image = db.Column(db.String(255)) # store image path
    
    is_featured = db.Column(db.Boolean, default=False)
    
    create_at = db.Column(db.DateTime, default=db.func.now())
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)