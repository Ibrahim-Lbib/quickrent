# browse, search
from flask import Blueprint, render_template
from app.models.listing import Listing

listing_bp = Blueprint('listing', __name__)

@listing_bp.route('/listings')
def listings():
    fake_properties = [
        {"title": "Cozy Room", "location": "Kampala", "price": "UGX 300K", "type": "single-room", "image": "static/listings/single-room-01.avif"},
        {"title": "Nice Apartment", "location": "Ntinda", "price": "UGX 900K", "type": "apartment", "image": "static/listings/apartment-01.jpg"},
        # add more...
    ]
    properties = fake_properties
    return render_template('listings.html', properties=properties)

@listing_bp.route('/listings/listings_detail')
def listing_detail():
    return render_template('listing_detail.html')