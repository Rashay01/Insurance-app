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
from routes.classic_cars_quote_bp import classic_cars_quote_bp

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
app.register_blueprint(classic_cars_quote_bp,url_prefix="/quote")

from models.classic_cars import ClassicCars
from models.policy import Policy

@app.route("/all-polices")
def all_policies():
    data = Select(Policy,ClassicCars).join(ClassicCars,Policy.policy_number ==ClassicCars.policy_number).order_by(Policy.policy_date.desc())
    filtered_policies = db.session.execute(data).fetchall()
    if(len(filtered_policies)==0):
        return "<h2>You have no policies</h2>"
    all_policies_data = {
        "classic_car": filtered_policies
    } 
    return render_template("all-polices.html", curr_page="all polices", all_policies_data=all_policies_data)



@app.route("/dashboard")
def dashboard():
    print(lg_user)
    return render_template("dashboard.html", curr_page="dashboard", user=lg_user)

#-----------------------------------------------------------------------------------------all policies pages
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
@app.get("/testing")
def testing_app():
    cars_quote = Select(Policy,ClassicCars).join(ClassicCars,Policy.policy_number ==ClassicCars.policy_number).filter_by(customer_id=lg_user["ID"]).order_by(Policy.policy_date.desc())
    result = db.session.execute(cars_quote).fetchall()
    print(result)
    # category = Category.query.get(result[1].category_id)
    # if category is None:
    #     return "<h2>Category is not found</h2>"
    # print(category.to_dict())
    return jsonify({"hi":"hi"})



try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)