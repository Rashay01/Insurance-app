from flask import Blueprint, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField
from wtforms.validators import InputRequired, Length, Regexp
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from extensions import db
from models.users import User

user_bp = Blueprint("user", __name__)


class RegistrationForm(FlaskForm):
    user_id = StringField(
        "ID Number",
        validators=[
            InputRequired(),
            Length(min=13, max=13),
            Regexp("^\d{13}$", message="Must be a valid ID with 13 digits only"),
        ],
    )
    name = StringField(
        "Name",
        validators=[
            InputRequired(),
            Length(min=1),
            Regexp("^[A-Za-z ]+$", message="Alpha numeric characters only"),
        ],
    )
    surname = StringField(
        "Surname",
        validators=[
            InputRequired(),
            Length(min=1),
            Regexp("^[A-Za-z ]+$", message="Alpha numeric characters only"),
        ],
    )
    email = EmailField("Email", validators=[InputRequired(), Length(min=8)])
    cell_no = StringField(
        "Phone Number",
        validators=[
            InputRequired(),
            Length(min=10),
            Regexp("^(\+\d{2})?\d{10}$", message="Valid cellphone with numbers"),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=8, max=12),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$",
                message="Valid password with at least one uppercase letter, one lowercase letter, one number and one special character '@$!%*?&'",
            ),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_user_id(self, field):
        user_found = User.query.get(field.data)
        if user_found:
            raise ValidationError("Account with ID taken")


class LoginForm(FlaskForm):
    ID = StringField("ID Number", validators=[InputRequired(), Length(min=5)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Login")

    def validate_ID(self, field):
        found_user = User.query.filter_by(ID=field.data).first()
        if not found_user:
            raise ValidationError("Invalid Credentials")

    def validate_password(self, field):
        found_user = User.query.filter_by(ID=self.ID.data).first()
        if found_user:
            user_found = found_user.to_dict()
            if not check_password_hash(user_found["password"], field.data):
                raise ValidationError("Invalid Credentials")


@user_bp.route("/registration", methods=["GET", "POST"])
def registration_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        data = {
            "ID": form.user_id.data,
            "name": form.name.data.strip(),
            "surname": form.surname.data.strip(),
            "email": form.email.data,
            "cell_no": form.cell_no.data,
            "password": generate_password_hash(form.password.data),
        }
        try:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered successfully")
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            return render_template(
                "Error-message.html",
                message="Server Error",
                status_code="500",
                error_options=None,
            )

    return render_template("registration.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(ID=form.ID.data).first()
        login_user(user)
        flash("Logged in successfully")
        return redirect("/dashboard")
    return render_template("login.html", form=form)
