# subscribe, payment processing
from flask import Blueprint, render_template, session, request
from flask_login import login_required


payments = Blueprint("payments", __name__)


@payments.route("/checkout")
@login_required
def checkout():
    plan = (request.args.get("plan") or session.get("selected_plan") or "").strip().lower()
    plan_info = {
        "pro": {"label": "Pro Plan", "price": "UGX 50K/month"},
        "agency": {"label": "Agency Plan", "price": "UGX 120K/month"},
    }
    return render_template("checkout.html", selected_plan=plan, plan_badge=plan_info.get(plan))

