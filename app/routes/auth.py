# login, register
from os import name
from os import name
from flask import Blueprint, redirect, render_template, request, url_for, flash
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('auth/register.html')
        
        hashed_password = generate_password_hash(password)
        
        if not all([full_name, email, phone, password]):
            flash('Please fill in all fields', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template('auth/register.html')
        
        user = User(
            full_name=full_name, 
            email=email, 
            phone=phone, 
            password_hash=hashed_password
            )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash("Account created successfully!", "success")
        return redirect(url_for('public.home'))
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not all([email, password]):
            flash('Please enter both email and password', 'error')
            return render_template('auth/login.html')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('public.home'))
        flash('Invalid credentials')
            
    return render_template('auth/login.html')

@auth_bp.context_processor
def inject_user():
    return dict(current_user=current_user)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    listings = current_user.listings
    return render_template('agent/dashboard.html', listings=listings)