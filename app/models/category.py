from app.extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationship
    listings = db.relationship('Listing', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
