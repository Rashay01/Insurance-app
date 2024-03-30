from flask import Blueprint, jsonify, request, current_app
from app import User,users

users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def get_users():
    user_list = User.query.all()  # Select * from movies
    data = [
        user.to_dict() for user in user_list
    ] 
    return jsonify(data)


@users_bp.get("/<id>")
def get_specific_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    return jsonify(user.to_dict())


@users_bp.put("/<id>")
def update_specific_user(id):
    user_update = request.json
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    user.update(user_update)
    return jsonify(user)


@users_bp.delete("/<id>")
def delete_specific_user(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    users.remove(user)
    return jsonify(user)


@users_bp.post("/")
def add_user():
    new_user = request.json
    found_user = next(
        (user for user in users if user["id"] == new_user.get("id", None)), None
    )
    if found_user:
        return jsonify({"message": "User ID already exists"}), 409
    users.append(new_user)
    return jsonify(new_user), 201
