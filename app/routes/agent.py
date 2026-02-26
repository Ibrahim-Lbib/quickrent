# dashboard, post listing
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services import listing_service

agent_bp = Blueprint("agent", __name__, url_prefix="/agent")


@agent_bp.route("/dashboard")
@login_required
def dashboard():
    listings = listing_service.get_agent_listings(current_user.id)
    return render_template(
        "agent/dashboard.html", 
        listings=listings,
        listings_count=len(listings)
        )
    
@agent_bp.route("/listing/new", methods=["GET", "POST"])
@login_required
def add_listing():
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
    
    return render_template("agent/add_listing.html") 

@agent_bp.route("/listing/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    listing = listing_service.get_listing_or_404(listing_id)
    if listing.user_id != current_user.id:
        flash("You don't have permission to edit this listing.", "error")
        return redirect(url_for("agent.dashboard"))
    
    if request.method == "POST":
        try:
            updated_listing = listing_service.update_listing(
                listing=listing,
                form_data=request.form,
                image_file=request.files.get("image")
            )
            flash("Listing updated", "success")
            return redirect(url_for("public.listing_detail", listing_id=listing.id))  
        except Exception as e:
            flash(str(e), "error")
    
    return render_template("agent/edit_listing.html", listing=listing)

@agent_bp.route("/listings/<int:listing_id>/delete", methods=["POST"])
@login_required
def delete_listing(listing_id):
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