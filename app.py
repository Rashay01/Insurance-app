import os
from flask import Flask, jsonify, request, render_template, redirect, flash
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, func
from dotenv import load_dotenv
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField
from wtforms.validators import InputRequired, Length
from datetime import datetime


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
connection_string = os.environ.get("DATABASE_STRING_TO_CONNECT")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)

users = [
    {
        "id": "0101165410081",
        "name": "Rashay",
        "surname": "Daya",
        "email": "rashay.jcdaya@gmail.com",
        "password": "Password01",
    },
    {
        "id": "0101165410082",
        "name": "Rashay1",
        "surname": "Daya1",
        "email": "rashay.jcdaya@gmail.com1",
        "password": "Password1!",
    },
]

policies = [
    {
        "id": 1,
        "user_id": "0101165410081",
        "date": "2023-01-3",
        "price": 1798,
        "num_years": 5,
        "active": True,
        "items": [
            {
                "id": 1,
                "name": "watch",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
    {
        "id": 2,
        "user_id": "0101165410081",
        "date": "2023-01-4",
        "price": 2000,
        "num_years": 5,
        "active": True,
        "items": [
            {
                "id": 1,
                "name": "Car",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
    {
        "id": 3,
        "user_id": "0101165410082",
        "date": "2023-01-3",
        "price": 1798,
        "num_years": 5,
        "active": True,
        "items": [
            {
                "id": 1,
                "name": "watch",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
]

quotes = [
    {
        "id": 1,
        "user_id": "0101165410081",
        "date": "2023-01-3",
        "price": 1798,
        "num_years": 5,
        "status": "accepted",
        "items": [
            {
                "id": 1,
                "name": "watch",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
    {
        "id": 2,
        "user_id": "0101165410081",
        "date": "2023-01-4",
        "price": 2000,
        "num_years": 5,
        "status": "waiting",
        "items": [
            {
                "id": 1,
                "name": "Car",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
    {
        "id": 3,
        "user_id": "0101165410082",
        "date": "2023-01-3",
        "price": 1798,
        "num_years": 5,
        "status": "declined",
        "items": [
            {
                "id": 1,
                "name": "watch",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
    {
        "id": 4,
        "user_id": "0101165410081",
        "date": "2023-01-3",
        "price": 1798,
        "num_years": 5,
        "status": "declined",
        "items": [
            {
                "id": 1,
                "name": "watch",
                "item_price": 30009,
                "description": "a vintage watch",
            }
        ],
    },
]

lg_user = {'ID': '0101165410081', 'name': 'Rashay', 'surname': 'Daya', 'email': 'rashay.jcdaya@gmail.com', 'cell_no': '0836681148', 'password': 'password01'}


class User(db.Model):
    __tablename__ = "users"
    ID = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # should be 50
    surname = db.Column(db.String(50), nullable=False)  # should be 50
    email = db.Column(db.String(50), nullable=False)  # should be 50
    cell_no = db.Column(db.String(50), nullable=False)  # should be 50
    password = db.Column(db.String(100), nullable=False)

    # JSON - Keys
    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "cell_no":self.cell_no,
            "password": self.password,
        }

class Quote(db.Model):
    __tablename__ = "quote"
    quote_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    quote_date = db.Column(db.String(50), nullable= False, default= func.now())
    quoted_premium = db.Column(db.Float, nullable=False)
    quote_decision_date = db.Column(db.String(50))
    status = db.Column(db.String(30))
    customer_id = db.Column(db.String(50), nullable = False) #varchar(50) Not Null FOREIGN KEY REFERENCES users(ID)

    def to_dict(self):
        return{
            "quote_id":self.quote_id,
            "quote_date":self.quote_date,
            "quoted_premium":self.quoted_premium,
            "quote_decision_date":self.quote_decision_date,
            "status":self.status,
            "customer_id":self.customer_id,
        }
    
class Item(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id= db.Column(db.Integer, nullable=False) #int NOT NULL FOREIGN KEY REFERENCES category(category_id),
    item_name = db.Column(db.String(50), nullable =False)
    item_desc = db.Column(db.String(500))
    item_value = db.Column(db.Float, nullable=False)
    policy_id = db.Column(db.String(50)) #FOREIGN KEY REFERENCES policy(policy_id),
    quote_id = db.Column(db.String(50), nullable=False) # FOREIGN KEY REFERENCES quote(quote_id)

    def to_dict(self):
        return{
            "item_id":self.item_id,
            "category_id":self.category_id,
            "item_name":self.item_name,
            "item_desc":self.item_desc,
            "item_value":self.item_value,
            "policy_id":self.policy_id,
            "quote_id":self.quote_id,
        }

from users_bp import users_bp
from quotes_bp import quotes_bp
from items_bp import items_bp

#REST API's
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(quotes_bp, url_prefix="/quotes")
app.register_blueprint(items_bp, url_prefix="/items")


@app.route("/")
def home():
    return render_template("landing.html", curr_page="home")


@app.route("/about/")
def about():
    return render_template("about.html", curr_page="about")


@app.route("/contact")
def contact():
    return render_template("contact.html", curr_page="contact")



@app.route("/dashboard")
def dashboard():
    print(lg_user)
    return render_template("dashboard.html", curr_page="dashboard", user=lg_user)

# class QuoteForm(FlaskForm):
# 	customer_id varchar(50) Not Null FOREIGN KEY REFERENCES users(ID)


@app.route('/quote', methods=["GET","POST"])
def new_claim():
    return render_template('new-quote.html')


# all policies pages
@app.route("/all-polices")
def all_policies():
    filtered_policies = [
        policy for policy in policies if policy["user_id"] == lg_user["ID"]
    ]
    data = sorted(filtered_policies, key=lambda x: x["active"], reverse=True)
    return render_template("all-polices.html", curr_page="all polices", polices=data)


@app.route("/all-polices/<id>", methods=["POST", "GET"])
def specific_policies(id):
    filtered_policy = next(
        (policy for policy in policies if policy["id"] == int(id)), None
    )
    if filtered_policy is None:
        return "<h2>404 Page not found</h2>"
    if request.method == "POST":
        days_after = date.today() + timedelta(days=30)
        filtered_policy.update({"active": False, "end_date": days_after})
        flash("Policy Removed")
        return redirect("/all-polices")
    else:

        return render_template(
            "policy.html", curr_page="all polices", policy=filtered_policy
        )

#----------------------------------------------------------------------------------User Registration
class RegistrationForm(FlaskForm):
    user_id = StringField("ID Number", validators=[InputRequired(), Length(min=13, max=13)])
    name = StringField("Name", validators=[InputRequired(),Length(min=1)])
    surname = StringField("Surname", validators=[InputRequired(),Length(min=1)])
    email = EmailField("Email", validators=[InputRequired(),Length(min=8)])
    cell_no = StringField("Phone Number", validators=[InputRequired(),Length(min=8)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    def validate_user_id(self, field):
        user_found = User.query.get(field.data)
        if user_found:
            raise ValidationError("Username taken")


@app.route("/registration", methods=["GET", "POST"])
def registration_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        data = {
            'ID': form.user_id.data,
            'name': form.name.data,
            'surname': form.surname.data,
            'email': form.email.data,
            'cell_no': form.cell_no.data,
            'password': form.password.data,
        }
        try:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            return f"<h2>Error Occurred {e}</h2>" 

    return render_template("registration.html", form=form)

#-----------------------------------TODO------------------------------------------------------User Login

class LogInForm(FlaskForm):
    lg_user_id = StringField("ID Number", validators=[InputRequired(),Length(min=1)])
    lg_password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8)]
    )
    loggin = SubmitField("Sign Up")




@app.route("/login", methods=["GET", "POST"])
def log_in_page():
    form = LogInForm()
    if request.method =="POST":
         logged_in_user = User.query.get("0101165410081").to_dict()
         lg_user.update(logged_in_user)
         
         return redirect('/dashboard')
         print(form.validate_on_submit())
         if form.validate_on_submit():
            return redirect("/")
   

    return render_template("login.html", form=form)
#-------------------------------------------------------------------------------------------------------
# @app.route("/all-polices", methods=["POST"])
# def remove_specific_policies(id):
#     filtered_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
#     policies.remove(filtered_policy)
#     return render_template("all-polices.html", curr_page="all polices", polices=policies)


# ------------------------------------------------------Policies-----------------------------------------


@app.get("/policies")
def get_policies():
    return jsonify(policies)


@app.get("/policies/<id>")
def get_specific_policy(id):
    policy = next((policy for policy in policies if policy["id"] == id), None)
    if policy is None:
        return jsonify({"message": "policy Not found"}), 404
    return jsonify(policy)


@app.put("/policies/<id>")
def update_specific_policy(id):
    policy_update = request.json
    user = next((policy for policy in policies if policy["id"] == id), None)
    if user is None:
        return jsonify({"message": "policy Not found"}), 404
    user.update(policy_update)
    return jsonify(user)


@app.delete("/policies/<id>")
def delete_specific_policy(id):
    policy = next((policy for policy in policies if policy["id"] == id), None)
    if policy is None:
        return jsonify({"message": "policy Not found"}), 404
    users.update(policy)
    return jsonify(policy)


@app.post("/policies")
def add_policy():
    policy = request.json
    users.append(policy)
    return jsonify(policy)




