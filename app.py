from flask import Flask, jsonify, request, render_template, redirect, flash
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

users = [
    {
        "id": "0101165410081",
        "name": "Rashay",
        "surname": "Daya",
        "email": "rashay.jcdaya@gmail.com",
        "password": "Pass01",
    },
    {
        "id": "0101165410082",
        "name": "Rashay1",
        "surname": "Daya1",
        "email": "rashay.jcdaya@gmail.com1",
        "password": "Pass011",
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


@app.route("/")
def home():
    return render_template("landing.html", curr_page="home")


@app.route("/about")
def about():
    return render_template("about.html", curr_page="about")


@app.route("/contact")
def contact():
    return render_template("contact.html", curr_page="contact")


# next two methods are for logging in
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", curr_page="login")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    id_num = request.form.get("id_num")
    password = request.form.get("password")
    filtered_user = next(
        (
            user
            for user in users
            if (user["id"] == id_num) and (user["password"] == password)
        ),
        None,
    )
    if filtered_user is None:
        return redirect("/login")
    lg_user.update(filtered_user)
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


# @app.route("/all-polices", methods=["POST"])
# def remove_specific_policies(id):
#     filtered_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
#     policies.remove(filtered_policy)
#     return render_template("all-polices.html", curr_page="all polices", polices=policies)

# -------------------------------------------------------Users-------------------------------------------


@app.get("/users")
def get_users():
    return jsonify(users)


@app.get("/users/<id>")
def get_specific_user(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    return jsonify(user)


@app.put("/users/<id>")
def update_specific_user(id):
    user_update = request.json
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    user.update(user_update)
    return jsonify(user)


@app.delete("/users/<id>")
def delete_specific_user(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    users.update(user)
    return jsonify(user)


@app.post("/users")
def add_user():
    new_user = request.json
    users.append(new_user)
    return jsonify(new_user), 201


# ------------------------------------------------------Policies-------------------------------------------


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
