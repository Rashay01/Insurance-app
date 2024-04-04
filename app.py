import os
from flask import Flask, jsonify, request, render_template, redirect, flash
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, func, Select
from dotenv import load_dotenv
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField, SelectField, FloatField, IntegerField, DateField
from wtforms.validators import InputRequired, Length 
from extensions import db


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
connection_string = os.environ.get("DATABASE_STRING_TO_CONNECT1")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db.init_app(app)





lg_user = {'ID': '0101165410081', 'name': 'Rashay', 'surname': 'Daya', 'email': 'rashay.jcdaya@gmail.com', 'cell_no': '0836681148', 'password': 'password01'}

# lg_user={}



# category_tup =[] 
   
# def populate_categories_tuple():
#     global category_tup
#     category_tup = [
#         (category.to_dict()['category_id'], category.to_dict()['category_name']) for category in Category.query.all()
#     ]
    
        


# Blue Prints imports
from routes.users_bp import users_bp
from routes.quotes_bp import quotes_bp
from routes.classic_car import classic_car_bp
from routes.category_bp import category_bp
from routes.policies_bp import policies_bp
from routes.cars_quote_bp import cars_quote_bp
from routes.main_bp import main_bp
from routes.user_bp import user_bp

#REST API's
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(quotes_bp, url_prefix="/quotes")
app.register_blueprint(classic_car_bp, url_prefix="/classic-car")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(policies_bp, url_prefix="/policies")
app.register_blueprint(cars_quote_bp, url_prefix="/cars-quote")

# # Html DIsplays jinja Templates
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

from models.cars_quote import CarQuote
from models.category import Category
from models.classic_cars import ClassicCars
from models.quote import Quote
class ClassicCarsForm(FlaskForm):
    vehicle_make = StringField("vehicle make",validators=[InputRequired(),Length(min=1)])
    model = StringField("model",validators=[InputRequired()])
    year_model = IntegerField("year model",validators=[InputRequired()])
    vin = StringField("vin",validators=[InputRequired()])
    license_plate_number = StringField("license_plate_number",validators=[InputRequired()])
    odometer_reading = IntegerField("odometer_reading",validators=[InputRequired()])
    fuel_type = StringField("fuel_type",validators=[InputRequired()])
    color = StringField("color",validators=[InputRequired()])
    current_value = FloatField("current_value",validators=[InputRequired()])
    year_purchased = DateField("year_purchased",format="%Y-%m-%d",validators=[InputRequired()])
    new_item = SubmitField("Get Quote")
    
    def validate_item_value(self, field):
        if field.data <= 0:
            ValidationError("Amount should be grater than zero")
            
@app.route('/quote/classic-cars', methods=["GET","POST"])
def get_new_quote():
    form = ClassicCarsForm()
    if form.validate_on_submit():
        category_data = Category.query.filter_by(category_name ="classic cars").first()
        category = category_data.to_dict()
        vehicle_id = str(uuid.uuid4())
        quote_id = str(uuid.uuid4())
        current_value = form.current_value.data
        cal_value = current_value*category['premium_percentage']
        data = {
            "vehicle_id": vehicle_id,
            "vehicle_make": form.vehicle_make.data,
            "model": form.model.data,
            "year_model":str(form.year_model.data),
            "vin":form.vin.data,
            "license_plate_number":form.license_plate_number.data,
            "odometer_reading":form.odometer_reading.data,
            "fuel_type":form.fuel_type.data,
            "color":form.color.data,
            "customer_id":lg_user['ID'],
            "current_value":current_value,
            "year_purchased":form.year_purchased.data.strftime('%Y-%m-%d' )
        }
        print(data)
        quote_data = {
            "quote_id":quote_id,
            "quoted_premium":cal_value,
            "status": "Deciding",
            "category_id":category["category_id"],
        }
        car_quote_data = {
            "vehicle_id": vehicle_id,
            "quote_id":quote_id
        } 
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
            return redirect('/dashboard')
        except Exception as e:
            db.session.rollback()
            return f"<h2>Error {e}</h2>"
    return render_template('new-classic-cars-quote.html', form=form)


@app.route("/dashboard")
def dashboard():
    print(lg_user)
    return render_template("dashboard.html", curr_page="dashboard", user=lg_user)

# -----------------------------------------------------------------------------------Quotes



# @app.route('/quote', methods=["GET","POST"])
# def get_new_quote():
#     populate_categories_tuple()
#     forms = QuoteForm()
#     if request.method == "POST" and forms.validate_on_submit():
#         try:
#             category_selected = request.form.get("category")
#             category = Category.query.get(category_selected).to_dict()

#             item_value = forms.item_value.data
#             quote_premium = item_value*category['premium_percentage']
#             quote_id = str(uuid.uuid4())
#             quote = {
#                 "quote_id" : quote_id,
#                 "quoted_premium" : quote_premium,
#                 "status" : "Deciding",
#                 "customer_id": lg_user["ID"],
#             }
#             item = {
#                 "category_id":category_selected,
#                 "item_name":forms.item_name.data,
#                 "item_desc":forms.item_description.data,
#                 "item_value":item_value,
#                 "quote_id":quote_id,
#             }
#             new_quote = Quote(**quote)
#             new_item = Item(**item)
#             db.session.add(new_quote)
#             db.session.commit()
#             db.session.add(new_item)
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             return f"<h2>Error</h2><p>{str(e)}</p>"
#         return f"<h1>Success {category_selected} {quote_premium}</h1>"
#     return render_template('new-quote.html', form=forms, cat_choice=category_tup)

# @app.route('/all-quotes')
# def get_all_user_quotes():
#     new_data = Select(Quote).join(Item,Quote.quote_id==Item.quote_id).distinct().where(Quote.customer_id =="0101165410081").order_by(Quote.quote_id)
#     result = db.session.execute(new_data).fetchall()
#     if len(result)==0:
#         return jsonify({"Message":"No Quotes found"})
    
#     quotes_data = []
#     for quote in result:
#         data = Item.query.filter_by(quote_id=quote[0].quote_id)
#         ans = [(item.to_dict()['item_id'], item.to_dict()['item_name']) for item in data ]
#         quotes_data.append([quote[0], ans])
#     return render_template('all-quotes.html',quotes_data= quotes_data)

# @app.route('/all-quotes/<id>')
# def get_single_user_quote(id):
#     data = Quote.query.get(id)
#     if data is None:
#         return "<h2>Quote not found </h2>"
#     quote = data.to_dict()
#     it_data = Item.query.filter_by(quote_id=id)
#     print(it_data)
#     items = [item.to_dict() for item in it_data]
#     if len(items)==0:
#         return "<h2>Query has no items</h2>"
#     return render_template('quote.html',quote= quote, items=items)

# -----------------------------------------------------------------------------------------all policies pages
# @app.route("/all-polices")
# def all_policies():
#     filtered_policies = [
#         policy for policy in policies if policy["user_id"] == lg_user["ID"]
#     ]
#     data = sorted(filtered_policies, key=lambda x: x["active"], reverse=True)
#     return render_template("all-polices.html", curr_page="all polices", polices=data)


# @app.route("/all-polices/<id>", methods=["POST", "GET"])
# def specific_policies(id):
#     filtered_policy = next(
#         (policy for policy in policies if policy["id"] == int(id)), None
#     )
#     if filtered_policy is None:
#         return "<h2>404 Page not found</h2>"
#     if request.method == "POST":
#         days_after = date.today() + timedelta(days=30)
#         filtered_policy.update({"active": False, "end_date": days_after})
#         flash("Policy Removed")
#         return redirect("/all-polices")
#     else:

#         return render_template(
#             "policy.html", curr_page="all polices", policy=filtered_policy
#         )


# @app.route("/all-polices", methods=["POST"])
# def remove_specific_policies(id):
#     filtered_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
#     policies.remove(filtered_policy)
#     return render_template("all-polices.html", curr_page="all polices", polices=policies)



# @app.get("/testing")
# def testing_app():
#     #TODO JOin 
#     new_data = Select(Quote).join(Item,Quote.quote_id==Item.quote_id).distinct().where(Quote.customer_id =="0101165410081").order_by(Quote.quote_id)
#     result = db.session.execute(new_data).fetchall()
#     if len(result)==0:
#         return jsonify({"Message":"No Quotes found"})

    
#     quotes_data = []
#     for quote in result:
#         data = Item.query.filter_by(quote_id=quote[0].quote_id)
#         ans = [(item.to_dict()['item_id'], item.to_dict()['item_name']) for item in data ]
#         quotes_data.append([quote[0], ans])

#     print(quotes_data)
#     return jsonify({"yes":"yes"}) 

# from models.cars_quote import CarQuote
# @app.get("/testing")
# def testing_app():
#     cars_quote = CarQuote.query.get({'vehicle_id':'as1234-12asd12','quote_id':'qt-001'})
#     if cars_quote is None:
#         return jsonify({"message": "Cars Quote link Not found"}), 404
#     return jsonify(cars_quote.to_dict())



try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)