import os
import uuid
from flask import current_app
from app.extensions import db
from app.models.listing import Listing
from app.services.whatsapp_service import normalize_phone, is_valid_phone

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "avif"}


# ------------------------------------------------------------------ #
# Image handling                                                       #
# ------------------------------------------------------------------ #

def allowed_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file) -> str | None:
    """Save uploaded image, return stored filename or None on failure."""
    if not file or not file.filename:
        return None
    if not allowed_image(file.filename):
        raise ValueError("Invalid image format. Use JPG, PNG, WEBP, or AVIF.")

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(current_app.root_path, "static", "images", "listings")
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return filename


def delete_image(filename: str):
    """Delete an image file from disk if it exists."""
    if not filename:
        return
    path = os.path.join(
        current_app.root_path, "static", "images", "listings", filename
    )
    if os.path.exists(path):
        os.remove(path)


# ------------------------------------------------------------------ #
# CRUD                                                                 #
# ------------------------------------------------------------------ #

def create_listing(form_data: dict, image_file, user_id: int) -> Listing:
    """
    Validate form data, save image, persist listing.
    Raises ValueError with a user-facing message on bad input.
    """
    title = form_data.get("title", "").strip()
    location = form_data.get("location", "").strip()
    whatsapp = form_data.get("whatsapp", "").strip()
    description = form_data.get("description", "").strip() or "No description provided."

    if not all([title, location, whatsapp]):
        raise ValueError("Title, location, and WhatsApp number are required.")

    if not is_valid_phone(whatsapp):
        raise ValueError("Enter a valid Ugandan phone number (e.g. 0701234567).")

    try:
        price = int(form_data.get("price", "").replace(",", "").replace(" ", ""))
        if price <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        raise ValueError("Price must be a positive number.")

    image_filename = save_image(image_file) if image_file and image_file.filename else None

    listing = Listing(
        title=title,
        description=description,
        price=price,
        type=form_data.get("category", "").strip(),
        location=location,
        whatsapp=normalize_phone(whatsapp),  # store normalized for clean wa.me links
        image=image_filename,
        user_id=user_id,
    )

    db.session.add(listing)
    db.session.commit()
    return listing


def update_listing(listing: Listing, form_data: dict, image_file) -> Listing:
    """Update a listing's fields. Replaces image if a new one is uploaded."""
    title = form_data.get("title", "").strip()
    location = form_data.get("location", "").strip()
    whatsapp = form_data.get("whatsapp", "").strip()

    if not all([title, location, whatsapp]):
        raise ValueError("Title, location, and WhatsApp number are required.")

    if not is_valid_phone(whatsapp):
        raise ValueError("Enter a valid Ugandan phone number.")

    try:
        price = int(form_data.get("price", "").replace(",", "").replace(" ", ""))
    except (ValueError, AttributeError):
        raise ValueError("Price must be a positive number.")

    listing.title = title
    listing.description = form_data.get("description", "").strip() or listing.description
    listing.price = price
    listing.type = form_data.get("category", listing.type)
    listing.location = location
    listing.whatsapp = normalize_phone(whatsapp)

    if image_file and image_file.filename:
        old_image = listing.image
        listing.image = save_image(image_file)
        delete_image(old_image)  # clean up old file

    db.session.commit()
    return listing


def delete_listing(listing: Listing):
    """Delete a listing and its associated image."""
    delete_image(listing.image)
    db.session.delete(listing)
    db.session.commit()


# ------------------------------------------------------------------ #
# Queries                                                              #
# ------------------------------------------------------------------ #

def get_listing_or_404(listing_id: int) -> Listing:
    return Listing.query.get_or_404(listing_id)


def get_agent_listings(user_id: int) -> list[Listing]:
    return (
        Listing.query
        .filter_by(user_id=user_id)
        .order_by(Listing.created_at.desc())
        .all()
    )


def get_featured_listings(limit: int = 6) -> list[Listing]:
    return (
        Listing.query
        .filter_by(is_featured=True)
        .order_by(Listing.created_at.desc())
        .limit(limit)
        .all()
    )