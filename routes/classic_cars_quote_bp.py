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
)
from wtforms.validators import InputRequired, Length
from models.cars_quote import CarQuote
from models.category import Category
from models.classic_cars import ClassicCars
from models.quote import Quote
from models.policy import Policy
import uuid
from extensions import db
from app import lg_user

classic_cars_quote_bp = Blueprint("classic_cars_quote", __name__)


class ClassicCarsForm(FlaskForm):
    vehicle_make = StringField(
        "vehicle make", validators=[InputRequired(), Length(min=1)]
    )
    model = StringField("model", validators=[InputRequired()])
    year_model = IntegerField("year model", validators=[InputRequired()])
    vin = StringField("vin", validators=[InputRequired()])
    license_plate_number = StringField(
        "license_plate_number", validators=[InputRequired()]
    )
    odometer_reading = IntegerField("odometer_reading", validators=[InputRequired()])
    fuel_type = StringField("fuel_type", validators=[InputRequired()])
    color = StringField("color", validators=[InputRequired()])
    current_value = FloatField("current_value", validators=[InputRequired()])
    year_purchased = DateField(
        "year_purchased", format="%Y-%m-%d", validators=[InputRequired()]
    )
    new_item = SubmitField("Get Quote")

    def validate_item_value(self, field):
        if field.data <= 0:
            ValidationError("Amount should be grater than zero")


@classic_cars_quote_bp.route("/classic-cars", methods=["GET", "POST"])
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
            "year_model": str(form.year_model.data),
            "vin": form.vin.data,
            "license_plate_number": form.license_plate_number.data,
            "odometer_reading": form.odometer_reading.data,
            "fuel_type": form.fuel_type.data,
            "color": form.color.data,
            "customer_id": lg_user["ID"],
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
            return f"<h2>Error {e}</h2>"
    return render_template("new-classic-cars-quote.html", form=form, lg_user=lg_user)


@classic_cars_quote_bp.route("/all-quotes")
def get_all_user_quotes():
    cars_quote = (
        Select(CarQuote, Quote, ClassicCars)
        .join(Quote, CarQuote.quote_id == Quote.quote_id)
        .join(ClassicCars, CarQuote.vehicle_id == ClassicCars.vehicle_id)
        .filter_by(customer_id=lg_user["ID"])
        .filter(Quote.status == "Deciding")
        .order_by(Quote.quote_date.desc())
    )
    result = db.session.execute(cars_quote).fetchall()
    if len(result) == 0:
        return "<h2>You have no existing quotes</h2>"
    return render_template("all-quotes.html", quotes_data=result, lg_user=lg_user)


@classic_cars_quote_bp.route("/all-quotes/<id>")
def get_single_user_quote(id):
    data = (
        Select(CarQuote, Quote, ClassicCars)
        .join(Quote, CarQuote.quote_id == Quote.quote_id)
        .join(ClassicCars, CarQuote.vehicle_id == ClassicCars.vehicle_id)
        .filter_by(customer_id=lg_user["ID"])
        .filter(Quote.quote_id == id)
    )
    result = db.session.execute(data).first()
    if len(result) == 0:
        return "<h2>Quote not found</h2>"
    category = Category.query.get(result[1].category_id)
    if category is None:
        return "<h2>Category is not found</h2>"
    return render_template(
        "quote.html",
        quote=result[1],
        item=result[2],
        category=category.to_dict(),
        lg_user=lg_user,
    )


@classic_cars_quote_bp.route("/quote/delete", methods=["POST"])
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
        return "<h2>500 Server Error</h2>"


@classic_cars_quote_bp.route("/quote/accept", methods=["POST"])
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
        return "<h2>500 Server Error</h2>"
