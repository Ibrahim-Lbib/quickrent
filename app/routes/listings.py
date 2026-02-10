# browse, search
from flask import Blueprint, render_template

listing_bp = Blueprint('listing', __name__)

@listing_bp.route('/listings')
def listings():
    return render_template('listings.html')