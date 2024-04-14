from flask import Blueprint, jsonify, request
from models.users import User
from extensions import db
from flask_login import login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)


@users_bp.get("/login_user_api")
def login_test():
    id = request.json.get("id")
    password = request.json.get("password")

    user = User.query.get(id)
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@users_bp.get("/")
@login_required
def get_users():
    user_list = User.query.all()
    data = [user.to_dict() for user in user_list]
    return jsonify(data)


@users_bp.get("/<id>")
@login_required
def get_specific_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    return jsonify(user.to_dict())


@users_bp.put("/<id>")
@login_required
def update_specific_user(id):
    user_update = request.json
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    try:
        for key, value in user_update.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        result = {"message": "User updated successfully", "data": user.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@users_bp.delete("/<id>")
@login_required
def delete_specific_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    try:
        data = user.to_dict()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User successfully deleted", "data": data})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@users_bp.post("/")
@login_required
def add_user():
    data = request.json
    password = data.get("password", None)
    new_user = User(**data)
    if password:
        has_pass = generate_password_hash(password)
        new_user.password = has_pass
    try:
        db.session.add(new_user)
        db.session.commit()
        result = {"message": "User added successfully", "data": new_user.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500
