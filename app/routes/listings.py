# browse, search
import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from app.models.listing import Listing
from app.extensions import db

listing_bp = Blueprint('listing', __name__, url_prefix='/dashboard')

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "avif", "gif"}

def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _save_image(file):
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = os.path.join(current_app.root_path, "static", "listings", "listings")
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, filename))
    return filename

@listing_bp.route('/listings')
@login_required
def listings():
    agent_listings = Listing.query.filter_by(user_id=current_user.id).order_by(Listing.created_at.desc()).all()
    return render_template('listings.html', listings=agent_listings)

@listing_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_listing():
    if request.method == "POST":
        title = request.form.get("title").strip()
        price = request.form.get("price").strip()
        category = request.form.get("category").strip()
        location = request.form.get("location").strip()
        description = request.form.get("description").strip()
        whatsapp = request.form.get("whatsapp").strip()
        image_file = request.files.get("image")
        
        if not all([title, price, category, location, description, whatsapp]):
            flash("Title, price, location, and WhatsApp number are required.", "error")
            return render_template('agent/add_listing.html')
        
        image_filename = None
        if image_file and image_file.filename:
            if not _allowed_file(image_file.filename):
                flash("Invalid image format. Use JPG, JPEG, PNG, WEBP, AVIF or GIF.", "error")
                return render_template('agent/add_listing.html')
            image_filename = _save_image(image_file)
            
        try:
            price_int = int(price.replace(",", "").replace(" ", ""))
        except ValueError:
            flash("Price must be a valid number.", "error")
            return render_template('agent/add_listing.html')
        
        listing = Listing(
            title=title,
            price=price_int,
            type=category,
            location=location,
            description=description or "No description provided.",
            whatsapp=whatsapp,
            image=image_filename,  # In a real app, you'd save the file and store the path
            user_id=current_user.id
        )
        
        db.session.add(listing)
        db.session.commit()
        
        flash("Listing created successfully!", "success")
        return redirect(url_for('auth.dashboard'))
    
    return render_template('agent/add_listing.html')

@listing_bp.route('/listings/<int:listing_id>/', methods=['GET'])
def listing_detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('agent/listing_detail.html', listing=listing)