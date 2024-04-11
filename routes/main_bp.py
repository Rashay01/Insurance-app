from flask import Blueprint, render_template
from app import lg_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("landing.html", curr_page="home", lg_user=lg_user)


@main_bp.route("/about/")
def about():
    return render_template("about.html", curr_page="about", lg_user=lg_user)


@main_bp.route("/contact")
def contact():
    return render_template("contact.html", curr_page="contact", lg_user=lg_user)


@main_bp.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html", curr_page="dashboard", user=lg_user, lg_user=lg_user
    )
