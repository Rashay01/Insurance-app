from flask import Blueprint, render_template, redirect, flash
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, EmailField
from wtforms.validators import InputRequired, Length, Regexp
from extensions import db
from app import lg_user

account_bp = Blueprint("account", __name__)


class EmailForm(FlaskForm):
    email = EmailField("New Email", validators=[InputRequired()])
    submit = SubmitField("Save Changes")


class ContactForm(FlaskForm):
    cont_num = StringField(
        "New Contact number",
        validators=[
            InputRequired(),
            Length(min=10),
            Regexp("^(\+\d{2})?\d{10}$", message="Valid cellphone with numbers"),
        ],
    )
    submit = SubmitField("Save Changes")


class PasswordForm(FlaskForm):
    user_id = ""
    password = StringField(
        "Old password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    new_password = StringField(
        "New password",
        validators=[
            InputRequired(),
            Length(min=8, max=12),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$",
                message="Valid password with at least one uppercase letter, one lowercase letter, one number and one special character '@$!%*?&'",
            ),
        ],
    )
    submit = SubmitField("Save Changes")

    def validate_password(self, field):
        print(field.data)
        user = User.query.get(self.user_id)
        if user is None:
            ValidationError("Server Error")
        if not check_password_hash(user.password, field.data):
            flash("Incorrect Old password")
            raise ValidationError("Invalid old password")

    def update_user_id(self, user):
        self.user_id = user


@account_bp.route("/account", methods=["POST", "GET"])
def user_account_page():
    email_form = EmailForm()
    contact_form = ContactForm()
    password_form = PasswordForm()

    user = User.query.get(lg_user["ID"])
    password_form.update_user_id(lg_user["ID"])

    if email_form.validate_on_submit():
        try:
            user.email = email_form.email.data
            db.session.commit()
            flash("Email changed successfully")
            return redirect("/account")
        except Exception as e:
            db.session.rollback()
            return render_template(
                "Error-message.html",
                lg_user=lg_user,
                message="Server Error",
                status_code="500",
                error_options=None,
            )

    if contact_form.validate_on_submit():
        try:
            user.cell_no = contact_form.cont_num.data
            db.session.commit()
            flash("Cell Number changed successfully")
            return redirect("/account")
        except Exception as e:
            db.session.rollback()
            return render_template(
                "Error-message.html",
                lg_user=lg_user,
                message="Server Error",
                status_code="500",
                error_options=None,
            )

    if password_form.validate_on_submit():
        try:
            hash_password = generate_password_hash(password_form.new_password.data)
            user.password = hash_password
            db.session.commit()
            flash("Password changed successfully")
            # return redirect("/account")
        except Exception as e:
            db.session.rollback()
            return render_template(
                "Error-message.html",
                lg_user=lg_user,
                message="Server Error",
                status_code="500",
                error_options=None,
            )

    return render_template(
        "account.html",
        user=user,
        email_form=email_form,
        contact_form=contact_form,
        password_form=password_form,
        lg_user=lg_user,
    )


@account_bp.route("/logout", methods=["POST"])
def logout():
    lg_user.clear()
    flash("Logged out successfully")
    return redirect("/")
