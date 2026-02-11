# homepage, landing pages
from flask import Blueprint, app, render_template
from app.models.listing import Listing

public = Blueprint("public", __name__)

@public.route('/')
def home():
    listings = Listing.query.order_by(Listing.created_at.desc()).limit(10).all()
    return render_template('home.html', listings=listings)

@public.route('/listings')
def listings():
    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template('listings.html', listings=listings)

@public.route('/listings/<int:listing_id>')
def listing_detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('listing_detail.html', listing=listing)