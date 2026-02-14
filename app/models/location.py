# areas in Kampala
from app.extensions import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    listings = db.relationship('Listing', backref='location', lazy=True)