from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    EmailField,

)
from wtforms.validators import InputRequired, Length,Regexp
from sqlalchemy.sql import Select
from models.classic_cars import ClassicCars
from models.policy import Policy
from extensions import db

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
    data = (
        Select(Policy, ClassicCars)
        .join(ClassicCars, Policy.policy_number == ClassicCars.policy_number)
        .filter_by(customer_id=current_user.ID)
        .order_by(Policy.active.desc(), Policy.policy_date.desc())
    )
    filtered_policies = db.session.execute(data).first()
    if filtered_policies is None:
        return render_template("dashboard.html", curr_page="dashboard", user=current_user, policy={},classic_car={})
    print(filtered_policies)
    return render_template("dashboard.html", curr_page="dashboard", user=current_user, policy=filtered_policies[0],classic_car=filtered_policies[1])
