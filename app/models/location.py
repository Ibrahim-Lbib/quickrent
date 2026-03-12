from app.extensions import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship
    listings = db.relationship('Listing', backref='location', lazy=True)

    def __repr__(self):
        return f'<Location {self.name}>'
