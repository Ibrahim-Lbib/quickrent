# login, register
from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    plan = (request.args.get("plan") or session.get("selected_plan") or "").strip().lower()
    allowed_plans = {"free", "pro", "agency"}
    if plan not in allowed_plans:
        plan = ""

    plan_info = {
        "free": {"label": "Free Plan", "price": "UGX 0/month"},
        "pro": {"label": "Pro Plan", "price": "UGX 50K/month"},
        "agency": {"label": "Agency Plan", "price": "UGX 120K/month"},
    }

    selected_role = "tenant"

    if request.method == "GET" and plan:
        session["selected_plan"] = plan

    if request.method == 'POST':
        full_name = request.form.get("full_name").strip()
        email = request.form.get("email").strip().lower()
        phone = (request.form.get("phone") or "").strip()
        password = request.form.get("password")
        role = (request.form.get("role") or "tenant").strip().lower()
        if role not in {"tenant", "agent"}:
            role = "tenant"
        selected_role = role

        if plan in {"pro", "agency"} and role != "agent":
            flash("Paid plans are for agents. Please select 'I'm listing a property'.", "error")
            return render_template('auth/register.html', selected_plan=plan, plan_badge=plan_info.get(plan), selected_role=selected_role)
        
        if not all([full_name, email, password]):
            flash('Please fill in all fields', 'error')
            return render_template('auth/register.html', selected_plan=plan, plan_badge=plan_info.get(plan), selected_role=selected_role)

        if role == "agent" and not phone:
            flash("WhatsApp number is required for agents.", "error")
            return render_template('auth/register.html', selected_plan=plan, plan_badge=plan_info.get(plan), selected_role=selected_role)
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('auth/register.html', selected_plan=plan, plan_badge=plan_info.get(plan), selected_role=selected_role)
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template('auth/register.html', selected_plan=plan, plan_badge=plan_info.get(plan), selected_role=selected_role)
        
        user = User(
            full_name=full_name, 
            email=email, 
            phone=phone or None,
            role=role,
            password_hash=generate_password_hash(password)
            )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash("Account created successfully!", "success")

        selected_plan = session.get("selected_plan")
        if selected_plan in {"pro", "agency"}:
            return redirect(url_for("payments.checkout", plan=selected_plan))

        if role == "agent":
            flash("Welcome! Post your first listing to start getting leads.", "success")
            return redirect(url_for("agent.dashboard"))

        flash("Welcome! Start browsing listings.", "success")
        return redirect(url_for("public.listings"))
    
    return render_template('auth/register.html', selected_plan=plan, plan_badge=plan_info.get(plan), selected_role=selected_role)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        next_url = (request.form.get("next") or "").strip()
        
        if not all([email, password]):
            flash('Please enter both email and password', 'error')
            return render_template('auth/login.html')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for('agent.dashboard'))
        flash('Invalid email or password', 'error')
            
    next_url = (request.args.get("next") or "").strip()
    redirect_message = ""
    if next_url.startswith("/agent/listing/new"):
        redirect_message = "Log in to post your property. You'll be taken back to the listing form after signing in."
    elif next_url.startswith("/agent"):
        redirect_message = "Log in to access your dashboard. You'll be taken back after signing in."
    elif next_url:
        redirect_message = "Log in to continue. You'll be taken back to where you left off after signing in."

    return render_template('auth/login.html', next=next_url, redirect_message=redirect_message)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        if not email:
            flash("Please enter your email address.", "error")
            return redirect(url_for("auth.forgot_password"))
        flash("If that email exists, we'll send reset instructions shortly.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")

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

@auth_bp.context_processor
def inject_user():
    return dict(current_user=current_user)
