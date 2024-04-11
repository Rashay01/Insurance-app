from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("landing.html", curr_page="home")


@main_bp.route("/about/")
def about():
    return render_template("about.html", curr_page="about")


@main_bp.route("/contact")
def contact():
    return render_template("contact.html", curr_page="contact")


@main_bp.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html", curr_page="dashboard", user=current_user)
