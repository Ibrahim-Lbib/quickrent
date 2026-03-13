import json

from app.extensions import db
from app.models.listing import Listing
from app.services.whatsapp_service import normalize_phone, is_valid_phone

from app.services.storage_service import StorageService

storage_service = StorageService()

def create_listing(form_data: dict, user_id: int, image_files=None, image_file=None) -> Listing:
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

    def _parse_non_negative_int(value, field_label: str) -> int:
        if value is None or str(value).strip() == "":
            return 0
        try:
            parsed = int(str(value).strip())
        except ValueError as exc:
            raise ValueError(f"{field_label} must be a whole number.") from exc
        if parsed < 0:
            raise ValueError(f"{field_label} cannot be negative.")
        return parsed

    bedrooms = _parse_non_negative_int(
        form_data.get("bedrooms", form_data.get("bedroom")),
        "Bedrooms",
    )
    bathrooms = _parse_non_negative_int(
        form_data.get("bathrooms", form_data.get("bathroom")),
        "Bathrooms",
    )

    nearby_landmarks = None
    raw_landmarks = form_data.get("nearby_landmarks")
    if raw_landmarks:
        try:
            nearby_landmarks = json.loads(raw_landmarks)
        except json.JSONDecodeError as exc:
            raise ValueError("Nearby landmarks must be valid JSON.") from exc
        if not isinstance(nearby_landmarks, list):
            raise ValueError("Nearby landmarks must be a JSON list.")
        for item in nearby_landmarks:
            if not isinstance(item, dict) or not str(item.get("name", "")).strip():
                raise ValueError("Each nearby landmark must be an object with a non-empty 'name'.")

    uploads = []
    if image_files:
        uploads = [f for f in list(image_files) if f and getattr(f, "filename", "")]
    elif image_file and getattr(image_file, "filename", ""):
        uploads = [image_file]

    image_filenames = [storage_service.save_image(f) for f in uploads]
    image_filenames = [n for n in image_filenames if n]
    image_filename = ",".join(image_filenames) if image_filenames else None

    listing = Listing(
        title=title,
        description=description,
        price=price,
        category_id=int(category_id),
        location_id=int(location_id),
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        nearby_landmarks=nearby_landmarks,
        has_electricity=bool(form_data.get("has_electricity")),
        has_water=bool(form_data.get("has_water")),
        has_wifi=bool(form_data.get("has_wifi")),
        has_security=bool(form_data.get("has_security")),
        has_parking=bool(form_data.get("has_parking")),
        whatsapp=normalize_phone(whatsapp),
        image=image_filename,
        user_id=user_id,
    )

    db.session.add(listing)
    db.session.commit()
    return listing


def update_listing(listing: Listing, form_data: dict, image_files=None, image_file=None) -> Listing:
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

    # Bedrooms/bathrooms are optional on edit to avoid overwriting if the UI doesn't provide them.
    if "bedrooms" in form_data or "bedroom" in form_data:
        listing.bedrooms = int((form_data.get("bedrooms") or form_data.get("bedroom") or 0))
    if "bathrooms" in form_data or "bathroom" in form_data:
        listing.bathrooms = int((form_data.get("bathrooms") or form_data.get("bathroom") or 0))

    if "nearby_landmarks" in form_data:
        raw_landmarks = form_data.get("nearby_landmarks") or ""
        if raw_landmarks.strip() == "":
            listing.nearby_landmarks = None
        else:
            try:
                parsed_landmarks = json.loads(raw_landmarks)
            except json.JSONDecodeError as exc:
                raise ValueError("Nearby landmarks must be valid JSON.") from exc
            if not isinstance(parsed_landmarks, list):
                raise ValueError("Nearby landmarks must be a JSON list.")
            for item in parsed_landmarks:
                if not isinstance(item, dict) or not str(item.get("name", "")).strip():
                    raise ValueError("Each nearby landmark must be an object with a non-empty 'name'.")
            listing.nearby_landmarks = parsed_landmarks

    # Utilities default to False if keys are present as unchecked checkboxes.
    utility_keys = [
        "has_electricity",
        "has_water",
        "has_wifi",
        "has_security",
        "has_parking",
    ]
    for key in utility_keys:
        if key in form_data:
            setattr(listing, key, bool(form_data.get(key)))

    uploads = []
    if image_files:
        uploads = [f for f in list(image_files) if f and getattr(f, "filename", "")]
    elif image_file and getattr(image_file, "filename", ""):
        uploads = [image_file]

    if uploads:
        old_image = listing.image
        image_filenames = [storage_service.save_image(f) for f in uploads]
        image_filenames = [n for n in image_filenames if n]
        if image_filenames:
            listing.image = ",".join(image_filenames)

        if old_image:
            for name in [p.strip() for p in str(old_image).split(",") if p.strip()]:
                storage_service.delete_image(name)

    db.session.commit()
    return listing


def delete_listing(listing: Listing):
    """Delete a listing and its associated image."""
    if listing.image:
        for name in [p.strip() for p in str(listing.image).split(",") if p.strip()]:
            storage_service.delete_image(name)
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
