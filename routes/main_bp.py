from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    EmailField,

)
from wtforms.validators import InputRequired, Length,Regexp

main_bp = Blueprint("main", __name__)

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    cell_no = StringField("Cell Number", validators=[InputRequired(),Length(min=10, max=14),Regexp("^(\+\d{2})?\d{10}$", message="Invalid cellphone number"),])
    submit = SubmitField("Contact Me")


@main_bp.route("/")
def home():
    return render_template("landing.html")


@main_bp.route("/about/")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f"We will contact you soon")
    return render_template("contact.html", form=form)


@main_bp.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html", curr_page="dashboard", user=current_user)
