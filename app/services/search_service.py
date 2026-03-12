from app.models.listing import Listing

def search_listings(location_id=None, category_id=None, max_price=None):
    """
    Filter listings by location ID, category ID, and/or price.
    Returns a SQLAlchemy query.
    """
    query = Listing.query

    if location_id:
        try:
            query = query.filter(Listing.location_id == int(location_id))
        except (ValueError, TypeError):
            pass

    if category_id:
        try:
            query = query.filter(Listing.category_id == int(category_id))
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            # Clean price string (handle commas if any)
            price_val = int(str(max_price).replace(",", "").replace(" ", "").strip())
            query = query.filter(Listing.price <= price_val)
        except (ValueError, TypeError):
            pass

    return query.order_by(Listing.is_featured.desc(), Listing.created_at.desc())