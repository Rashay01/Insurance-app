#RESTFUL APIs for policy
from flask import Blueprint, jsonify, request
from flask_login import login_required
from models.policy import Policy
from extensions import db

policies_bp = Blueprint("policies", __name__)


@policies_bp.get("/")
@login_required
def get_policies():
    policies_list = Policy.query.all()
    data = [policy.to_dict() for policy in policies_list]
    return jsonify(data)


@policies_bp.get("/<id>")
@login_required
def get_specific_policies(id):
    policy = Policy.query.get(id)
    if policy is None:
        return jsonify({"message": "Policy Not found"}), 404
    return jsonify(policy.to_dict())


@policies_bp.put("/<id>")
@login_required
def update_specific_policies(id):
    policy_update = request.json
    policy = Policy.query.get(id)
    if policy is None:
        return jsonify({"message": "Policy Not found"}), 404
    try:
        for key, value in policy_update.items():
            if hasattr(policy, key):
                setattr(policy, key, value)
        db.session.commit()
        result = {"message": "Policy updated successfully", "data": policy.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@policies_bp.delete("/<id>")
@login_required
def delete_specific_policies(id):
    policy = Policy.query.get(id)
    if policy is None:
        return jsonify({"message": "Policy Not found"}), 404
    try:
        data = policy.to_dict()
        db.session.delete(policy)
        db.session.commit()
        return jsonify({"message": "Policy successfully deleted", "data": data})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@policies_bp.post("/")
@login_required
def add_policies():
    data = request.json
    new_policy = Policy(**data)
    try:
        db.session.add(new_policy)
        db.session.commit()
        result = {"message": "Policy added successfully", "data": new_policy.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500
