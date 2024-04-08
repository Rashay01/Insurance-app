from flask import Blueprint, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField
from wtforms.validators import InputRequired, Length 
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.users import User
from app import lg_user

user_bp = Blueprint("user", __name__)

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
            'ID': form.user_id.data,
            'name': form.name.data,
            'surname': form.surname.data,
            'email': form.email.data,
            'cell_no': form.cell_no.data,
            'password': generate_password_hash(form.password.data),
        }
        try:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            return f"<h2>Error Occurred {e}</h2>" 

    return render_template("registration.html", form=form,lg_user=lg_user)




@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(ID=form.ID.data).first()
        lg_user.update(user.to_dict())
        flash("Logged in successfully")
        return redirect('/dashboard')
    return render_template("login.html", form=form,lg_user=lg_user)