# homepage, landing pages
from flask import Blueprint, render_template, request
from app.models.listing import Listing
from app.services.search_service import search_listings

public = Blueprint("public", __name__)

@public.route('/')
def home():
    listings = Listing.query.order_by(
        Listing.is_featured.desc(), Listing.created_at.desc()
        ).limit(10).all()
    return render_template('home.html', listings=listings)

@public.route('/listings')
def listings():
    location = request.args.get("location", "").strip()
    property_type = request.args.get("type", "").strip()
    max_price = request.args.get("price", "").strip()
    
    query = search_listings(
        location=location or None,
        property_type=property_type or None,
        max_price=max_price or None,
    )
    listings = query.all()
    
    return render_template(
        "listings.html",
        listings=listings,
        selected_location=location,
        selected_type=property_type,
        selected_price=max_price,
    )

@public.route('/listings/<int:listing_id>')
def listing_detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('listing_detail.html', listing=listing)