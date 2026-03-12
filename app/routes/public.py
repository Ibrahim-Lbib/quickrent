# homepage, landing pages
from flask import Blueprint, render_template, request
from app.models.listing import Listing
from app.models.category import Category
from app.models.location import Location
from app.services.search_service import search_listings

public = Blueprint("public", __name__)

@public.route('/')
def home():
    listings = Listing.query.order_by(
        Listing.is_featured.desc(), Listing.created_at.desc()
        ).limit(10).all()
    categories = Category.query.all()
    locations = Location.query.all()
    return render_template('home.html', listings=listings, categories=categories, locations=locations)

@public.route('/listings')
def listings():
    location_id = request.args.get("location_id")
    category_id = request.args.get("category_id")
    max_price = request.args.get("price", "").strip()
    
    query = search_listings(
        location_id=location_id,
        category_id=category_id,
        max_price=max_price or None,
    )
    listings = query.all()
    
    categories = Category.query.all()
    locations = Location.query.all()
    
    return render_template(
        "listings.html",
        listings=listings,
        categories=categories,
        locations=locations,
        selected_location=location_id,
        selected_type=category_id,
        selected_price=max_price,
    )

@public.route('/listings/<int:listing_id>')
def listing_detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('listing_detail.html', listing=listing)