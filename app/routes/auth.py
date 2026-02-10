# login, register
from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

def register():
    return render_template('auth/register.html')
