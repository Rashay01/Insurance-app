from flask import Blueprint, jsonify, request, current_app
from app import User,db

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
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    try:
        for key, value in user_update.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        result = {"message": "updated successfully", "data": user.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500


@users_bp.delete("/<id>")
def delete_specific_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User Not found"}), 404
    try:
        data = user.to_dict()
        db.session.delete(user)
        db.session.commit()
        return jsonify(data)
    except Exception as e:
        db.session.rollback()  # undo the commit
        return {"message": str(e)}, 500


@users_bp.post("/")
def add_user():
    data = request.json
    new_user= User(**data)
    try:
        db.session.add(new_user)
        db.session.commit()
        result = {"message": "User added successfully", "data": new_user.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
