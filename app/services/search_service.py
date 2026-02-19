from app.models.listing import Listing


def search_listings(location=None, property_type=None, max_price=None):
    """
    Filter listings by location, type, and/or price.
    Returns a SQLAlchemy query so callers can chain .all(), .limit() etc.
    """
    query = Listing.query

    if location and location.strip():
        query = query.filter(Listing.location.ilike(f"%{location.strip()}%"))

    if property_type and property_type.strip():
        query = query.filter(Listing.type == property_type.strip())

    if max_price:
        try:
            query = query.filter(Listing.price <= int(max_price))
        except (ValueError, TypeError):
            pass  # ignore bad price input, return unfiltered

    return query.order_by(Listing.is_featured.desc(), Listing.created_at.desc())