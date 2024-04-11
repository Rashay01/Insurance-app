from flask import Blueprint, request, render_template, redirect, flash
from sqlalchemy.sql import func, Select
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    ValidationError,
    FloatField,
    IntegerField,
    DateField,
    SelectField,
)
from wtforms.validators import InputRequired, Length, Regexp
from models.cars_quote import CarQuote
from models.category import Category
from models.classic_cars import ClassicCars
from models.quote import Quote
from models.policy import Policy
import uuid
from extensions import db
from flask_login import current_user, login_required
from datetime import datetime

classic_cars_quote_bp = Blueprint("classic_cars_quote", __name__)

fuel_types_list = [("Petrol", "Petrol"), ("Diesel", "Diesel")]


class ClassicCarsForm(FlaskForm):
    vehicle_make = StringField(
        "vehicle make", validators=[InputRequired(), Length(min=1)]
    )
    model = StringField("model", validators=[InputRequired()])
    year_model = StringField(
        "year model",
        validators=[InputRequired(), Regexp("^\d{4}$", message="Enter a valid year")],
    )
    vin = StringField(
        "vin",
        validators=[
            InputRequired(),
            Length(min=17, max=17),
            Regexp("^[0-9A-HJ-NPR-Za-hj-npr-z]+$", message="Invalid VIN"),
        ],
    )
    license_plate_number = StringField(
        "License Plate Number",
        validators=[
            InputRequired(),
            Length(max=7),
            Regexp(
                "^[A-Za-z0-9]+$",
                message="Enter Valid License Plate Number with A-Z 0-9",
            ),
        ],
    )
    odometer_reading = IntegerField("odometer_reading", validators=[InputRequired()])
    fuel_type = SelectField(
        "fuel_type", validators=[InputRequired()], choices=fuel_types_list
    )
    color = StringField("color", validators=[InputRequired()])
    current_value = FloatField("current_value", validators=[InputRequired()])
    year_purchased = DateField(
        "year_purchased", format="%Y-%m-%d", validators=[InputRequired()]
    )
    new_item = SubmitField("Get Quote")

    def validate_current_value(self, field):
        if float(field.data) <= 0:
            raise ValidationError("Amount should be grater than zero")

    def validate_odometer_reading(self, field):
        if int(field.data) <= 0:
            raise ValidationError("Amount should be grater than zero")

    def validate_year_purchased(self, field):
        curr_date = datetime.now().date()
        if curr_date < field.data:
            raise ValidationError("Date must be before or equal to current date")

    def validate_year_model(self, field):
        curr_date = datetime.now().year
        try:
            date = int(field.data)
            if date <= 0:
                raise ValidationError("enter a positive year")
            if date > (curr_date - 25):
                raise ValidationError("We cover classic cars from 25 years ago")
        except Exception as e:
            raise ValidationError("Enter a year with Numbers (YYYY)")


@classic_cars_quote_bp.route("/classic-cars", methods=["GET", "POST"])
@login_required
def get_new_quote():
    form = ClassicCarsForm()
    if form.validate_on_submit():
        category_data = Category.query.filter_by(category_name="classic cars").first()
        category = category_data.to_dict()
        vehicle_id = str(uuid.uuid4())
        quote_id = str(uuid.uuid4())
        current_value = form.current_value.data
        cal_value = round(current_value * category["premium_percentage"], 2)
        data = {
            "vehicle_id": vehicle_id,
            "vehicle_make": form.vehicle_make.data,
            "model": form.model.data,
            "year_model": form.year_model.data,
            "vin": form.vin.data.upper(),
            "license_plate_number": form.license_plate_number.data.upper(),
            "odometer_reading": form.odometer_reading.data,
            "fuel_type": form.fuel_type.data,
            "color": form.color.data,
            "customer_id": current_user.ID,
            "current_value": current_value,
            "year_purchased": form.year_purchased.data.strftime("%Y-%m-%d"),
        }
        print(data)
        quote_data = {
            "quote_id": quote_id,
            "quoted_premium": cal_value,
            "status": "Deciding",
            "category_id": category["category_id"],
        }
        car_quote_data = {"vehicle_id": vehicle_id, "quote_id": quote_id}
        try:
            new_classic_car = ClassicCars(**data)
            new_quote = Quote(**quote_data)
            new_cars_quote = CarQuote(**car_quote_data)
            db.session.add(new_classic_car)
            db.session.commit()
            db.session.add(new_quote)
            db.session.commit()
            db.session.add(new_cars_quote)
            db.session.commit()
            flash("New Quote changed successfully")
            return redirect("/dashboard")
        except Exception as e:
            db.session.rollback()
            return render_template(
                "Error-message.html",
                message="Server Error",
                status_code="500",
                error_options=None,
            )
    return render_template("new-classic-cars-quote.html", form=form)


@classic_cars_quote_bp.route("/all-quotes")
@login_required
def get_all_user_quotes():
    cars_quote = (
        Select(CarQuote, Quote, ClassicCars)
        .join(Quote, CarQuote.quote_id == Quote.quote_id)
        .join(ClassicCars, CarQuote.vehicle_id == ClassicCars.vehicle_id)
        .filter_by(customer_id=current_user.ID)
        .filter(Quote.status == "Deciding")
        .order_by(Quote.quote_date.desc())
    )
    result = db.session.execute(cars_quote).fetchall()
    if len(result) == 0:
        return render_template(
            "Error-message.html",
            message="You have no existing quotes",
            error_options="quote",
        )
    return render_template("all-quotes.html", quotes_data=result)


@classic_cars_quote_bp.route("/all-quotes/<id>")
@login_required
def get_single_user_quote(id):
    data = (
        Select(CarQuote, Quote, ClassicCars)
        .join(Quote, CarQuote.quote_id == Quote.quote_id)
        .join(ClassicCars, CarQuote.vehicle_id == ClassicCars.vehicle_id)
        .filter_by(customer_id=current_user.ID)
        .filter(Quote.quote_id == id)
    )
    result = db.session.execute(data).first()
    if len(result) == 0:
        return render_template(
            "Error-message.html",
            message="Quote not found",
            status_code="404",
            error_options=None,
        )
    category = Category.query.get(result[1].category_id)
    if category is None:
        return render_template(
            "Error-message.html",
            message="Category Not Found",
            status_code="500",
            error_options=None,
        )
    return render_template(
        "quote.html",
        quote=result[1],
        item=result[2],
        category=category.to_dict(),
    )


@classic_cars_quote_bp.route("/quote/delete", methods=["POST"])
@login_required
def delete_classic_car_quote_user():
    quote_id = request.form.get("quote_id")
    try:
        quote = Quote.query.get(quote_id)
        quote.status = "Declined"
        quote.quote_decision_date = func.now()
        db.session.commit()
        flash("Quote declined")
        return redirect("/quote/all-quotes")
    except Exception as e:
        db.session.rollback()
        return render_template(
            "Error-message.html",
            message="Server Error",
            status_code="500",
            error_options=None,
        )


@classic_cars_quote_bp.route("/quote/accept", methods=["POST"])
@login_required
def accept_classic_car_quote_user():
    quote_id = request.form.get("quote_id")
    vehicle_id = request.form.get("vehicle_id")
    policy_id = str(uuid.uuid4())
    try:

        quote = Quote.query.get(quote_id)

        quote.status = "Accepted"
        quote.quote_decision_date = func.now()
        data = {
            "policy_number": policy_id,
            "monthly_premium": quote.quoted_premium,
            "category_id": quote.category_id,
        }
        policy = Policy(**data)
        db.session.add(policy)
        db.session.commit()
        classic_car = ClassicCars.query.get(vehicle_id)
        classic_car.policy_number = policy_id
        db.session.commit()
        flash("Quote Accepted")
        return redirect("/quote/all-quotes")
    except Exception as e:
        db.session.rollback()
        return render_template(
            "Error-message.html",
            message="Server Error",
            status_code="500",
            error_options=None,
        )
