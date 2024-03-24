from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

users=[
    {'id': '0101165410081',
     'name': "Rashay",
     'surname': 'Daya',
     'email': 'rashay.jcdaya@gmail.com',
     'password' : "Pass01",
    },
    {'id': '0101165410082',
     'name': "Rashay1",
     'surname': 'Daya1',
     'email': 'rashay.jcdaya@gmail.com1',
     'password' : "Pass011",
    },
]


@app.route("/")
def home():
    return render_template("landing.html", curr_page ="home")

@app.route("/about")
def about():
    return render_template("about.html", curr_page ="about")

@app.route("/contact")
def contact():
    return render_template("contact.html", curr_page ="contact")

#-------------------------------------------------------Users-------------------------------------------

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
    return jsonify(new_user)
#------------------------------------------------------Quotes-------------------------------------------