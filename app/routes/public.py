# homepage, landing pages
from flask import Blueprint, flash, redirect, render_template, request, url_for
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

    def _listings_url(location_id=None, category_id=None, price=None):
        return url_for(
            "public.listings",
            location_id=location_id or None,
            category_id=category_id or None,
            price=price or None,
        )

    clear_url = _listings_url()

    active_filters = []
    if category_id:
        cat_name = next((c.name for c in categories if str(c.id) == str(category_id)), str(category_id))
        active_filters.append(
            {"label": f"Type: {cat_name}", "remove_url": _listings_url(location_id, None, max_price)}
        )
    if location_id:
        loc_name = next((loc.name for loc in locations if str(loc.id) == str(location_id)), str(location_id))
        active_filters.append(
            {"label": f"Location: {loc_name}", "remove_url": _listings_url(None, category_id, max_price)}
        )
    if max_price:
        def _ugx_short(amount_str: str) -> str:
            try:
                amount = int(str(amount_str).replace(",", "").replace(" ", "").strip())
            except ValueError:
                return str(amount_str)
            if amount >= 1_000_000:
                m = amount / 1_000_000
                text = f"{m:.1f}".rstrip("0").rstrip(".")
                return f"UGX {text}M"
            if amount >= 1_000:
                return f"UGX {amount // 1_000}K"
            return f"UGX {amount}"

        active_filters.append(
            {"label": f"Max: {_ugx_short(max_price)}", "remove_url": _listings_url(location_id, category_id, None)}
        )
    
    return render_template(
        "listings.html",
        listings=listings,
        categories=categories,
        locations=locations,
        selected_location=location_id,
        selected_type=category_id,
        selected_price=max_price,
        clear_url=clear_url,
        active_filters=active_filters,
    )

@public.route('/listings/<int:listing_id>')
def listing_detail(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    def _gallery_images(listing_obj: Listing) -> list[str]:
        # Stored uploads currently use Listing.image as a filename (single image).
        # Support comma-separated filenames to allow future multi-image expansion.
        filenames: list[str] = []
        if getattr(listing_obj, "image", None):
            raw = str(listing_obj.image).strip()
            if raw:
                filenames = [p.strip() for p in raw.split(",") if p.strip()]

        if filenames:
            return [f"uploads/listings/{name}" for name in filenames]

        img_map = {
            "Single Room": "single-room-01.avif",
            "Hostel": "hostel-01.webp",
            "Apartment": "apartment-01.jpg",
            "Shop": "shop-01.jpg",
            "Office": "office-01.webp",
        }
        category_name = getattr(getattr(listing_obj, "category", None), "name", None)
        placeholder = img_map.get(category_name, "apartment-01.jpg")
        return [f"images/listings/{placeholder}"]

    return render_template(
        'listing_detail.html',
        listing=listing,
        gallery_images=_gallery_images(listing),
    )


@public.route("/contact", methods=["GET", "POST"])
def contact():
    subject = (request.args.get("subject") or "").strip()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        subject = (request.form.get("subject") or subject or "").strip()
        message = (request.form.get("message") or "").strip()

        if not name or not email or not message:
            flash("Please fill in name, email, and message.", "error")
            return redirect(url_for("public.contact"))

        # Placeholder: no email delivery wired up yet.
        flash("Thanks, we received your message. We'll get back to you shortly.", "success")
        return redirect(url_for("public.contact"))

    return render_template("contact.html", subject=subject)


def _coming_soon(title: str):
    return render_template("coming_soon.html", page_title=title)


@public.route("/privacy")
def privacy():
    return _coming_soon("Privacy Policy")


@public.route("/terms")
def terms():
    return _coming_soon("Terms of Service")


@public.route("/cookies")
def cookies():
    return _coming_soon("Cookie Policy")


@public.route("/accessibility")
def accessibility():
    return _coming_soon("Accessibility")


@public.route("/about")
def about():
    return _coming_soon("About Us")


@public.route("/blog")
def blog():
    return _coming_soon("Blog")
