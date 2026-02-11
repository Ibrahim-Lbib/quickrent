# browse, search
from flask import Blueprint, render_template

listing_bp = Blueprint('listing', __name__)

@listing_bp.route('/listings')
def listings():
    properties = [
        {
            'id': 1,
            'title': 'Cozy Single Room',
            'location': 'Makerere Kikoni',
            'price': 'UGX 250K',
            'image': 'single-room-01.avif',
            'type': 'single-room',
            'features': {'bedrooms': '1', 'bathrooms': '1'}
        },
        {
            'id': 2,
            'title': 'Modern Student Hostel',
            'location': 'Wandegeya',
            'price': 'UGX 350K',
            'image': 'hostel-01.webp',
            'type': 'hostel',
            'features': {'bedrooms': '1', 'bathrooms': 'Shared'}
        },
        {
            'id': 3,
            'title': '2-Bedroom Apartment',
            'location': 'Ntinda',
            'price': 'UGX 800K',
            'image': 'apartment-01.jpg',
            'type': 'apartment',
            'features': {'bedrooms': '2', 'bathrooms': '2'}
        },
        {
            'id': 4,
            'title': 'Retail Shop Space',
            'location': 'Nakawa Market',
            'price': 'UGX 600K',
            'image': 'shop-01.jpg',
            'type': 'shop'
        },
        {
            'id': 5,
            'title': 'Professional Office',
            'location': 'Kololo',
            'price': 'UGX 1.2M',
            'image': 'office-01.webp',
            'type': 'office',
            'features': {'bedrooms': 'N/A', 'bathrooms': '2'}
        },
        {
            'id': 6,
            'title': 'Premium Self-Contained',
            'location': 'Makerere',
            'price': 'UGX 400K',
            'image': 'single-room-01.jfif',
            'type': 'single-room',
            'features': {'bedrooms': '1', 'bathrooms': '1'}
        },
        {
            'id': 7,
            'title': 'Spacious Single Room',
            'location': 'Kikumi Kikumi',
            'price': 'UGX 280K',
            'image': 'single-room-02.jpg',
            'type': 'single-room',
            'features': {'bedrooms': '1', 'bathrooms': '1'}
        },
        {
            'id': 8,
            'title': 'Executive Hostel',
            'location': 'Kisaasi',
            'price': 'UGX 420K',
            'image': 'hostel-02.jpg',
            'type': 'hostel',
            'features': {'bedrooms': '1', 'bathrooms': 'Private'}
        },
        {
            'id': 9,
            'title': 'Luxury 3-Bedroom',
            'location': 'Najjera',
            'price': 'UGX 1.5M',
            'image': 'apartment-02.jpg',
            'type': 'apartment',
            'features': {'bedrooms': '3', 'bathrooms': '3'}
        },
        {
            'id': 10,
            'title': 'Modern Studio',
            'location': 'Bukoto',
            'price': 'UGX 500K',
            'image': 'apartment-03.jpg',
            'type': 'apartment',
            'features': {'bedrooms': 'Studio', 'bathrooms': '1'}
        },
        {
            'id': 11,
            'title': 'Commercial Office',
            'location': 'Industrial Area',
            'price': 'UGX 900K',
            'image': 'office-02.jpg',
            'type': 'office',
            'features': {'bedrooms': 'N/A', 'bathrooms': '2'}
        },
        {
            'id': 12,
            'title': 'Boutique Shop',
            'location': 'Acacia Mall',
            'price': 'UGX 750K',
            'image': 'shop-02.jpg',
            'type': 'shop'
        }
    ]
    return render_template('listings.html', properties=properties)