from flask import Blueprint, render_template

common_bp = Blueprint("common", __name__)

@common_bp.route("/")
def home():
    return render_template("landing.html", curr_page="home")


@common_bp.route("/about/")
def about():
    return render_template("about.html", curr_page="about")


@common_bp.route("/contact")
def contact():
    return render_template("contact.html", curr_page="contact")

