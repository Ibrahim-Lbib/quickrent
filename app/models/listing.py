# rooms, apartments, shops
from app.extensions import db

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    price = db.Column(db.Integer, nullable=False)
    
    image = db.Column(db.String(255)) # store image path
    
    # Property details
    type_deleted = db.Column(db.String(50), nullable=True) # temporary to avoid breaking too much before migration
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)

    # Optional structured info (shown on listing detail page when provided)
    nearby_landmarks = db.Column(db.JSON, nullable=True)  # list[{"name": str, "distance": str}]

    # Utilities (render only when True)
    has_electricity = db.Column(db.Boolean, default=False)
    has_water = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_security = db.Column(db.Boolean, default=False)
    has_parking = db.Column(db.Boolean, default=False)
    
    whatsapp = db.Column(db.String(20), nullable=False) # contact number
    
    is_featured = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    
    @property
    def agent_name(self):
        return self.agent.full_name if self.agent else "Unknown Agent"
    
    @property
    def agent_phone(self):
        return self.whatsapp
