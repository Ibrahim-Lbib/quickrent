from app.extensions import db
from app.models.listing import Listing
from app.services.whatsapp_service import normalize_phone, is_valid_phone

from app.services.storage_service import StorageService

storage_service = StorageService()

def create_listing(form_data: dict, image_file, user_id: int) -> Listing:
    """
    Validate form data, save image, persist listing.
    Raises ValueError with a user-facing message on bad input.
    """
    title = form_data.get("title", "").strip()
    category_id = form_data.get("category_id")
    location_id = form_data.get("location_id")
    whatsapp = form_data.get("whatsapp", "").strip()
    description = form_data.get("description", "").strip() or "No description provided."

    if not all([title, category_id, location_id, whatsapp]):
        raise ValueError("Title, Category, Location, and WhatsApp number are required.")

    if not is_valid_phone(whatsapp):
        raise ValueError("Enter a valid Ugandan phone number (e.g. 0701234567).")

    try:
        price = int(form_data.get("price", "").replace(",", "").replace(" ", ""))
        if price <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        raise ValueError("Price must be a positive number.")

    image_filename = storage_service.save_image(image_file) if image_file and image_file.filename else None

    listing = Listing(
        title=title,
        description=description,
        price=price,
        category_id=int(category_id),
        location_id=int(location_id),
        whatsapp=normalize_phone(whatsapp),
        image=image_filename,
        user_id=user_id,
    )

    db.session.add(listing)
    db.session.commit()
    return listing


def update_listing(listing: Listing, form_data: dict, image_file) -> Listing:
    """Update a listing's fields. Replaces image if a new one is uploaded."""
    title = form_data.get("title", "").strip()
    category_id = form_data.get("category_id")
    location_id = form_data.get("location_id")
    whatsapp = form_data.get("whatsapp", "").strip()

    if not all([title, category_id, location_id, whatsapp]):
        raise ValueError("Title, Category, Location, and WhatsApp number are required.")

    if not is_valid_phone(whatsapp):
        raise ValueError("Enter a valid Ugandan phone number.")

    try:
        price = int(form_data.get("price", "").replace(",", "").replace(" ", ""))
    except (ValueError, AttributeError):
        raise ValueError("Price must be a positive number.")

    listing.title = title
    listing.description = form_data.get("description", "").strip() or listing.description
    listing.price = price
    listing.category_id = int(category_id)
    listing.location_id = int(location_id)
    listing.whatsapp = normalize_phone(whatsapp)

    if image_file and image_file.filename:
        old_image = listing.image
        listing.image = storage_service.save_image(image_file)
        storage_service.delete_image(old_image)

    db.session.commit()
    return listing


def delete_listing(listing: Listing):
    """Delete a listing and its associated image."""
    storage_service.delete_image(listing.image)
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
