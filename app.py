import os
from flask import Flask, jsonify, request, render_template, redirect, flash
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, func, Select
from dotenv import load_dotenv
import uuid
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    EmailField,
    SelectField,
    FloatField,
    IntegerField,
    DateField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, login_required, login_user
from extensions import db


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
connection_string = os.environ.get("AZURE_CONNECTION_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login_page"

from models.users import User


@login_manager.user_loader
def load_user(ID):
    return User.query.filter_by(ID=ID).first()


# BluePrints imports
from routes.users_bp import users_bp
from routes.quotes_bp import quotes_bp
from routes.classic_car import classic_car_bp
from routes.category_bp import category_bp
from routes.policies_bp import policies_bp
from routes.cars_quote_bp import cars_quote_bp
from routes.claims_bp import claims_bp
from routes.claim_status_bp import claim_status_bp
from routes.main_bp import main_bp
from routes.user_bp import user_bp
from routes.classic_cars_quote_bp import classic_cars_quote_bp
from routes.classic_cars_policy_bp import classic_cars_policy_bp
from routes.account_bp import account_bp
from routes.all_claims_bp import all_claims_bp

# REST API's
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(quotes_bp, url_prefix="/quotes")
app.register_blueprint(classic_car_bp, url_prefix="/classic-car")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(policies_bp, url_prefix="/policies")
app.register_blueprint(cars_quote_bp, url_prefix="/cars-quote")
app.register_blueprint(claims_bp, url_prefix="/claims")
app.register_blueprint(claim_status_bp, url_prefix="/claims-status")

# # Html DIsplays jinja Templates
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(classic_cars_quote_bp, url_prefix="/quote")
app.register_blueprint(classic_cars_policy_bp, url_prefix="/all-policies")
app.register_blueprint(account_bp)
app.register_blueprint(all_claims_bp)


try:
    with app.app_context():
        result = db.session.execute(text("SELECT 1")).fetchall()
        # db.drop_all()
        # db.create_all()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)
