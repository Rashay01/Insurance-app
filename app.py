import os
from flask import Flask, jsonify, request, render_template, redirect, flash
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("MY_SECRET_KEY")

# connection_string = os.environ.get("AZURE_DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# db = SQLAlchemy(app)

# try:
#     with app.app_context():
#         # Use text() to explicitly declare your SQL command
#         result = db.session.execute(text("SELECT 1")).fetchall()
#         print("Connection successful:", result)
# except Exception as e:
#     print("Error connecting to the database:", e)

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

lg_user = {}


# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     username = db.Column(db.String(50), nullable=False, unique=True)  # should be 50
#     password = db.Column(db.String(100), nullable=False)

#     # JSON - Keys
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "username": self.username,
#             "password": self.password,
#         }


from users_bp import users_bp

app.register_blueprint(users_bp, url_prefix="/users")


@app.route("/")
def home():
    return render_template("landing.html", curr_page="home")


@app.route("/about/")
def about():
    return render_template("about.html", curr_page="about")


@app.route("/contact")
def contact():
    return render_template("contact.html", curr_page="contact")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Login")

    def validate_username(self, field):
        raise ValidationError("Username taken")

    def validate_password(self, field):
        raise ValidationError("Username taken")

    # def validate_id(self, field):
    #     print(field.value)
    #     # found_user = next((user for user in users if user["id"] == field.data), None)
    #     # if not found_user:
    #     raise ValidationError("Invalid Credentials")

    def validate_password(self, field):
        print(field.value)
        found_user = next(
            (
                user
                for user in users
                if (user["id"] == self.id.data) and (user["password"] == field.data)
            ),
            None,
        )
        if not found_user:
            raise ValidationError("Invalid Credentials")


# next two methods are for logging in
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        id_num = form.username.data
        filtered_user = next(
            (user for user in users if user["id"] == id_num),
            None,
        )
        if filtered_user:
            lg_user.update(filtered_user)
            return redirect("/dashboard")
    return render_template("login.html", curr_page="login", form=form)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", curr_page="dashboard", user=lg_user)


# all policies pages
@app.route("/all-polices")
def all_policies():
    filtered_policies = [
        policy for policy in policies if policy["user_id"] == lg_user["id"]
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


class RegistrationForm(FlaskForm):
    id = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    # def validate <field name>
    def validate_id(self, field):
        print(field.id)
        user_found = next((user for user in users if user["id"] == field.data), None)
        if user_found:
            raise ValidationError("Username taken")


@app.route("/registration", methods=["GET", "POST"])
def registration_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        return "<h2>Success</h2>"

    return render_template("registration.html", form=form)


# @app.route("/all-polices", methods=["POST"])
# def remove_specific_policies(id):
#     filtered_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
#     policies.remove(filtered_policy)
#     return render_template("all-polices.html", curr_page="all polices", polices=policies)

# -------------------------------------------------------Users-------------------------------------------


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


# ------------------------------------------------------Quotes-------------------------------------------


@app.get("/quotes")
def get_quote():
    return jsonify(quotes)


@app.get("/quotes/<id>")
def get_specific_quote(id):
    quote = next((quote for quote in quotes if quote["id"] == id), None)
    if quote is None:
        return jsonify({"message": "quotes Not found"}), 404
    return jsonify(quote)


@app.put("/quotes/<id>")
def update_specific_quote(id):
    policy_update = request.json()
    quote = next((quotes for quote in quotes if quote["id"] == id), None)
    if quote is None:
        return jsonify({"message": "quotes Not found"}), 404
    quote.update(policy_update)
    return jsonify(quote)


@app.delete("/quotes/<id>")
def delete_specific_quote(id):
    quote = next((quote for quote in quotes if quote["id"] == id), None)
    if quote is None:
        return jsonify({"message": "quote Not found"}), 404
    users.update(quote)
    return jsonify(quote)


@app.post("/quotes")
def add_quote():
    quote = request.json()
    users.append(quote)
    return jsonify(quote)
