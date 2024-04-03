import os
from flask import Flask, jsonify, request, render_template, redirect, flash
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, func, Select
from dotenv import load_dotenv
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField, SelectField, FloatField
from wtforms.validators import InputRequired, Length 
from extensions import db


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")
connection_string = os.environ.get("DATABASE_STRING_TO_CONNECT")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db.init_app(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


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


lg_user = {'ID': '0101165410081', 'name': 'Rashay', 'surname': 'Daya', 'email': 'rashay.jcdaya@gmail.com', 'cell_no': '0836681148', 'password': 'password01'}

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_desc = db.Column(db.String(500))
    premium_percentage = db.Column(db.Float, nullable= False)

    def to_dict(self):
        return{
            "category_id":self.category_id,
            "category_name":self.category_name,
            "category_desc":self.category_desc,
            "premium_percentage":self.premium_percentage,
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
    
class Policy(db.Model):
    __tablename__ = "policy"
    policy_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    policy_date = db.Column(db.DateTime, nullable=False)
    monthly_premium = db.Column(db.Float, nullable=False)
    policy_end_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default =True)
    customer_id = db.Column(db.String(50), nullable=False)#FOREIGN KEY REFERENCES users(ID)

    def to_dict(self):
        return{
            "policy_id":self.policy_id,
            "policy_date":self.policy_date,
            "monthly_premium":self.monthly_premium,
            "policy_end_date":self.policy_end_date,
            "active":self.active,
            "customer_id":self.customer_id,
        }

category_tup =[] 
   
def populate_categories_tuple():
    global category_tup
    category_tup = [
        (category.to_dict()['category_id'], category.to_dict()['category_name']) for category in Category.query.all()
    ]
    
        


# Blue Prints imports
from users_bp import users_bp
from quotes_bp import quotes_bp
from items_bp import items_bp
from category_bp import category_bp
from policies_bp import policies_bp
from common_bp import common_bp

#REST API's
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(quotes_bp, url_prefix="/quotes")
app.register_blueprint(items_bp, url_prefix="/items")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(policies_bp, url_prefix="/policies")

# Html DIsplays
app.register_blueprint(common_bp)





@app.route("/dashboard")
def dashboard():
    print(lg_user)
    return render_template("dashboard.html", curr_page="dashboard", user=lg_user)

# -----------------------------------------------------------------------------------Quotes
class QuoteForm(FlaskForm):
    item_name = StringField("Item Name",validators=[InputRequired(),Length(min=1)])
    item_description = StringField("Item Description")
    item_value = FloatField("Item Value")
    new_item = SubmitField("Get Quote")
    
    def validate_item_value(self, field):
        if field.data <= 0:
            ValidationError("Amount should be grater than zero")


@app.route('/quote', methods=["GET","POST"])
def get_new_quote():
    populate_categories_tuple()
    forms = QuoteForm()
    if request.method == "POST" and forms.validate_on_submit():
        try:
            category_selected = request.form.get("category")
            category = Category.query.get(category_selected).to_dict()

            item_value = forms.item_value.data
            quote_premium = item_value*category['premium_percentage']
            quote_id = str(uuid.uuid4())
            quote = {
                "quote_id" : quote_id,
                "quoted_premium" : quote_premium,
                "status" : "Deciding",
                "customer_id": lg_user["ID"],
            }
            item = {
                "category_id":category_selected,
                "item_name":forms.item_name.data,
                "item_desc":forms.item_description.data,
                "item_value":item_value,
                "quote_id":quote_id,
            }
            new_quote = Quote(**quote)
            new_item = Item(**item)
            db.session.add(new_quote)
            db.session.commit()
            db.session.add(new_item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"<h2>Error</h2><p>{str(e)}</p>"
        return f"<h1>Success {category_selected} {quote_premium}</h1>"
    return render_template('new-quote.html', form=forms, cat_choice=category_tup)

@app.route('/all-quotes')
def get_all_user_quotes():
    new_data = Select(Quote).join(Item,Quote.quote_id==Item.quote_id).distinct().where(Quote.customer_id =="0101165410081").order_by(Quote.quote_id)
    result = db.session.execute(new_data).fetchall()
    if len(result)==0:
        return jsonify({"Message":"No Quotes found"})
    
    quotes_data = []
    for quote in result:
        data = Item.query.filter_by(quote_id=quote[0].quote_id)
        ans = [(item.to_dict()['item_id'], item.to_dict()['item_name']) for item in data ]
        quotes_data.append([quote[0], ans])
    return render_template('all-quotes.html',quotes_data= quotes_data)

@app.route('/all-quotes/<id>')
def get_single_user_quote(id):
    data = Quote.query.get(id)
    if data is None:
        return "<h2>Quote not found </h2>"
    quote = data.to_dict()
    it_data = Item.query.filter_by(quote_id=id)
    print(it_data)
    items = [item.to_dict() for item in it_data]
    if len(items)==0:
        return "<h2>Query has no items</h2>"
    return render_template('quote.html',quote= quote, items=items)

# -----------------------------------------------------------------------------------------all policies pages
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
    loggin = SubmitField("Login")




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



@app.get("/testing")
def testing_app():
    #TODO JOin 
    new_data = Select(Quote).join(Item,Quote.quote_id==Item.quote_id).distinct().where(Quote.customer_id =="0101165410081").order_by(Quote.quote_id)
    result = db.session.execute(new_data).fetchall()
    if len(result)==0:
        return jsonify({"Message":"No Quotes found"})

    
    quotes_data = []
    for quote in result:
        data = Item.query.filter_by(quote_id=quote[0].quote_id)
        ans = [(item.to_dict()['item_id'], item.to_dict()['item_name']) for item in data ]
        quotes_data.append([quote[0], ans])

    print(quotes_data)
    return jsonify({"yes":"yes"}) 