# browse, search
from flask import Blueprint, render_template

listing_bp = Blueprint('listing', __name__)

@listing_bp.route('/listings')
def listings():
    return render_template('listings.html')

@listing_bp.route('/listings/listing_detail')
def listings_detail():
    return render_template('listing_detail.html')