from flask import Blueprint, render_template, redirect, flash
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, EmailField
from wtforms.validators import InputRequired, Length 
from extensions import db
from app import lg_user

account_bp = Blueprint("account", __name__)

class EmailForm(FlaskForm):
    email = EmailField("New Email", validators=[InputRequired()]) 
    submit = SubmitField("Save Changes")   

class ContactForm(FlaskForm):
    cont_num = StringField("New Contact number", validators=[InputRequired()]) 
    submit = SubmitField("Save Changes") 
    
class PasswordForm(FlaskForm):
    user_id =""
    password = StringField("Old password", validators=[InputRequired()]) 
    new_password = StringField("New password", validators=[InputRequired()]) 
    submit = SubmitField("Save Changes") 
    
    def validate_password(self,field):
        print(field.data)
        user = User.query.get(self.user_id)
        if user is None:
            ValidationError('Server Error')
        if not check_password_hash(user.password, field.data):
                raise ValidationError("Invalid old password")
        
    
    def update_user_id(self, user):
        self.user_id = user
        
      
@account_bp.route("/account", methods=["POST","GET"])
def user_account_page():
    email_form = EmailForm()
    contact_form = ContactForm()
    password_form = PasswordForm()
    
    user = User.query.get(lg_user['ID'])
    password_form.update_user_id(lg_user['ID'])
    
    if email_form.validate_on_submit():
        try:
            user.email = email_form.email.data
            db.session.commit()
            return redirect("/account")
        except Exception as e:
            db.session.rollback()
            return "<h2>500 Server Error</h2>"
    
    if contact_form.validate_on_submit():
        try:
            user.cell_no = contact_form.cont_num.data
            db.session.commit()
            return redirect("/account")
        except Exception as e:
            db.session.rollback()
            return "<h2>500 Server Error</h2>"
        
    if password_form.validate_on_submit():
        try:
            hash_password= generate_password_hash(password_form.new_password.data)
            user.password = hash_password
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return "<h2>500 Server Error</h2>"
    
    return render_template("account.html", user=user, email_form = email_form, contact_form=contact_form, password_form=password_form)
