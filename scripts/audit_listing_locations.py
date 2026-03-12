import argparse

from app import create_app
from app.extensions import db
from app.models.listing import Listing
from app.models.location import Location


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def infer_location_from_title(title: str, locations_by_norm_name: dict[str, Location]) -> Location | None:
    """
    Heuristic: if exactly one location name appears in the title (case-insensitive),
    treat it as the expected location. If none or multiple match, return None.
    """
    normalized_title = _normalize(title)
    matches: list[Location] = []
    for norm_name, loc in locations_by_norm_name.items():
        if norm_name and norm_name in normalized_title:
            matches.append(loc)
    if len(matches) == 1:
        return matches[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Listing.location_id against Listing.title and optionally apply fixes."
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Flask config name (dev/test/prod). Defaults to FLASK_ENV or 'dev'.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply suggested location_id updates.",
    )
    parser.add_argument(
        "--only-id",
        type=int,
        default=None,
        help="Only audit/apply to a single listing ID.",
    )

    args = parser.parse_args()

    app = create_app(args.config)
    with app.app_context():
        locations = Location.query.order_by(Location.name.asc()).all()
        locations_by_norm_name = {_normalize(loc.name): loc for loc in locations}

        query = Listing.query.order_by(Listing.id.asc())
        if args.only_id is not None:
            query = query.filter_by(id=args.only_id)
        listings = query.all()

        suggested_updates: list[tuple[int, str, str | None, str]] = []
        ambiguous: list[tuple[int, str]] = []
        no_match: list[tuple[int, str]] = []

        for listing in listings:
            expected = infer_location_from_title(listing.title, locations_by_norm_name)
            if expected is None:
                # Track whether it was ambiguous or just no-match.
                normalized_title = _normalize(listing.title)
                hits = [
                    loc.name
                    for norm_name, loc in locations_by_norm_name.items()
                    if norm_name and norm_name in normalized_title
                ]
                if len(hits) > 1:
                    ambiguous.append((listing.id, listing.title))
                else:
                    no_match.append((listing.id, listing.title))
                continue

            current_name = listing.location.name if listing.location else None
            if not listing.location or listing.location.id != expected.id:
                suggested_updates.append((listing.id, listing.title, current_name, expected.name))
                if args.apply:
                    listing.location_id = expected.id

        print(f"Locations in DB: {len(locations)}")
        print(f"Listings audited: {len(listings)}")
        print(f"Suggested fixes: {len(suggested_updates)}")
        if ambiguous:
            print(f"Ambiguous titles (skipped): {len(ambiguous)}")
        if no_match:
            print(f"No location in title (skipped): {len(no_match)}")

        if suggested_updates:
            print("\nSuggested updates:")
            for listing_id, title, old, new in suggested_updates:
                print(f"  id={listing_id} title={title!r}: {old!r} -> {new!r}")

        if args.apply and suggested_updates:
            db.session.commit()
            print("\nApplied updates.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

