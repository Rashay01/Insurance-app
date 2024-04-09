from flask import Blueprint, jsonify, request
from models.claim_status import ClaimStatus
from extensions import db

claim_status_bp = Blueprint("claims_status", __name__)


@claim_status_bp.get("/")
def get_claim_status():
    claim_status_list = ClaimStatus.query.all()
    data = [claim_status.to_dict() for claim_status in claim_status_list]
    return jsonify(data)


@claim_status_bp.get("/<id>")
def get_specific_claim_status(id):
    claim_status = ClaimStatus.query.get(id)
    if claim_status is None:
        return jsonify({"message": "Claim Status Not found"}), 404
    return jsonify(claim_status.to_dict())


@claim_status_bp.put("/<id>")
def update_specific_claim_status(id):
    claim_status_update = request.json
    claim_status = ClaimStatus.query.get(id)
    if claim_status is None:
        return jsonify({"message": "Claim Status Not found"}), 404
    try:
        for key, value in claim_status_update.items():
            if hasattr(claim_status, key):
                setattr(claim_status, key, value)
        db.session.commit()
        result = {
            "message": "Claim Status updated successfully",
            "data": claim_status.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@claim_status_bp.delete("/<id>")
def delete_specific_claim_status(id):
    claim_status = ClaimStatus.query.get(id)
    if claim_status is None:
        return jsonify({"message": "Claim Status Not found"}), 404
    try:
        data = claim_status.to_dict()
        db.session.delete(claim_status)
        db.session.commit()
        return jsonify({"message": "Claim Status successfully deleted", "data": data})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@claim_status_bp.post("/")
def add_claim_status():
    data = request.json
    new_claim_status = ClaimStatus(**data)
    try:
        db.session.add(new_claim_status)
        db.session.commit()
        result = {
            "message": "Claim Status added successfully",
            "data": new_claim_status.to_dict(),
        }
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500
