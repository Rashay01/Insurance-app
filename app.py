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
    
        


# BluePrints imports
from routes.users_bp import users_bp
from routes.quotes_bp import quotes_bp
from routes.classic_car import classic_car_bp
from routes.category_bp import category_bp
from routes.policies_bp import policies_bp
from routes.cars_quote_bp import cars_quote_bp
from routes.claims_bp import claims_bp

from routes.main_bp import main_bp
from routes.user_bp import user_bp
from routes.classic_cars_quote_bp import classic_cars_quote_bp
from routes.classic_cars_policy_bp import classic_cars_policy_bp
from routes.account_bp import account_bp

#REST API's
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(quotes_bp, url_prefix="/quotes")
app.register_blueprint(classic_car_bp, url_prefix="/classic-car")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(policies_bp, url_prefix="/policies")
app.register_blueprint(cars_quote_bp, url_prefix="/cars-quote")
app.register_blueprint(claims_bp, url_prefix="/claims")

# # Html DIsplays jinja Templates
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(classic_cars_quote_bp,url_prefix="/quote")
app.register_blueprint(classic_cars_policy_bp,url_prefix="/all-policies")
app.register_blueprint(account_bp)




@app.route("/dashboard")
def dashboard():
    print(lg_user)
    return render_template("dashboard.html", curr_page="dashboard", user=lg_user)




# from models.cars_quote import CarQuote
# @app.get("/testing")
# def testing_app():
#     cars_quote = Select(Policy,ClassicCars).join(ClassicCars,Policy.policy_number ==ClassicCars.policy_number).filter_by(customer_id=lg_user["ID"]).order_by(Policy.policy_date.desc())
#     result = db.session.execute(cars_quote).fetchall()
#     print(result)
#     # category = Category.query.get(result[1].category_id)
#     # if category is None:
#     #     return "<h2>Category is not found</h2>"
#     # print(category.to_dict())
#     return jsonify({"hi":"hi"})



try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)