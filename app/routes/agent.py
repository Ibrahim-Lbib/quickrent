# dashboard, post listing
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models.category import Category
from app.models.location import Location
from app.services import listing_service

agent_bp = Blueprint("agent", __name__, url_prefix="/agent")

@agent_bp.route("/dashboard")
@login_required
def dashboard():
    if getattr(current_user, "role", "agent") != "agent":
        flash("Log in as an agent to access the dashboard.", "error")
        return redirect(url_for("public.listings"))
    listings = listing_service.get_agent_listings(current_user.id)
    return render_template(
        "agent/dashboard.html", 
        listings=listings,
        listings_count=len(listings)
        )
    
@agent_bp.route("/listing/new", methods=["GET", "POST"])
@login_required
def add_listing():
    if getattr(current_user, "role", "agent") != "agent":
        flash("Log in as an agent to post a property.", "error")
        return redirect(url_for("public.listings"))
    if request.method == "POST":
        try:
            listing = listing_service.create_listing(
                form_data=request.form,
                image_file=request.files.get("image"),
                user_id=current_user.id
            )
            flash("Listing created successfully!", "success")
            return redirect(url_for("public.listing_detail", listing_id=listing.id))  
        except Exception as e:
            flash(str(e), "error")
    
    categories = Category.query.all()
    locations = Location.query.all()
    return render_template("agent/add_listing.html", categories=categories, locations=locations) 

@agent_bp.route("/listing/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    if getattr(current_user, "role", "agent") != "agent":
        flash("Log in as an agent to edit listings.", "error")
        return redirect(url_for("public.listings"))
    listing = listing_service.get_listing_or_404(listing_id)
    if listing.user_id != current_user.id:
        flash("You don't have permission to edit this listing.", "error")
        return redirect(url_for("agent.dashboard"))
    
    if request.method == "POST":
        try:
            listing_service.update_listing(
                listing=listing,
                form_data=request.form,
                image_file=request.files.get("image")
            )
            flash("Listing updated", "success")
            return redirect(url_for("public.listing_detail", listing_id=listing.id))  
        except Exception as e:
            flash(str(e), "error")
    
    categories = Category.query.all()
    locations = Location.query.all()
    return render_template("agent/edit_listing.html", listing=listing, categories=categories, locations=locations)

@agent_bp.route("/listings/<int:listing_id>/delete", methods=["POST"])
@login_required
def delete_listing(listing_id):
    if getattr(current_user, "role", "agent") != "agent":
        flash("Log in as an agent to manage listings.", "error")
        return redirect(url_for("public.listings"))
    listing = listing_service.get_listing_or_404(listing_id)

    if listing.user_id != current_user.id:
        flash("You don't have permission to delete this listing.", "error")
        return redirect(url_for("agent.dashboard"))

    listing_service.delete_listing(listing)
    flash("Listing deleted.", "success")
    return redirect(url_for("agent.dashboard"))

@agent_bp.route('/subscription')
def subscription():
    return render_template('agent/subscriptions.html')
