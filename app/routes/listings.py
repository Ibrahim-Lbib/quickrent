# browse, search
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.models.listing import Listing
from app.extensions import db

listing_bp = Blueprint('listing', __name__, url_prefix='/dashboard')

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

@listing_bp.route('/add', methods=['GET', 'POST'])
def add_listing():
    
    # must be logged in to add listing
    if "user_id" not in session:
        flash("Please log in to add a listing.", "error")
        return redirect(url_for('auth.login'))
    
    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        category = request.form.get("category")
        location = request.form.get("location")
        description = request.form.get("description")
        whatsapp = request.form.get("whatsapp")
        image = request.files.get("image")
        
        listing = Listing(
            title=title,
            price=price,
            category=category,
            location=location,
            description=description,
            whatsapp=whatsapp,
            image=image.filename,  # In a real app, you'd save the file and store the path
            user_id=session["user_id"]
        )
        
        db.session.add(listing)
        db.session.commit()
        
        flash("Listing created successfully!", "success")
        return redirect(url_for('auth.dashboard'))
    
    return render_template('agent/add_listing.html')