# single room, hostel, office
from app.extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    listings = db.relationship('Listing', backref='category', lazy=True)