from flask import Blueprint, jsonify, request, current_app
from app import users

users_bp = Blueprint("movies", __name__)


@users_bp.get("/users")
def get_users():
    return jsonify(users)


@users_bp.get("/users/<id>")
def get_specific_user(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    return jsonify(user)


@users_bp.put("/users/<id>")
def update_specific_user(id):
    user_update = request.json
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    user.update(user_update)
    return jsonify(user)


@users_bp.delete("/users/<id>")
def delete_specific_user(id):
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    users.update(user)
    return jsonify(user)


@users_bp.post("/users")
def add_user():
    new_user = request.json
    users.append(new_user)
    return jsonify(new_user), 201
