from flask import Blueprint, jsonify, request
from models.claim import Claim
from extensions import db

claims_bp = Blueprint("claims", __name__)

@claims_bp.get("/")
def get_claims():
    claim_list = Claim.query.all()
    data = [
        claim.to_dict() for claim in claim_list
    ] 
    return jsonify(data)


@claims_bp.get("/<id>")
def get_specific_claim(id):
    claim = Claim.query.get(id)
    if claim is None:
        return jsonify({"message": "Claim Not found"}), 404
    return jsonify(claim.to_dict())


@claims_bp.put("/<id>")
def update_specific_claim(id):
    claim_update = request.json
    claim = Claim.query.get(id)
    if claim is None:
        return jsonify({"message": "Claim Not found"}), 404
    try:
        for key, value in claim_update.items():
            if hasattr(claim, key):
                setattr(claim, key, value)
        db.session.commit()
        result = {"message": "Claim updated successfully", "data": claim.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return {"message": "Error occurred","Error": str(e)}, 500


@claims_bp.delete("/<id>")
def delete_specific_claim(id):
    claim = Claim.query.get(id)
    if claim is None:
        return jsonify({"message": "Claim Not found"}), 404
    try:
        data = claim.to_dict()
        db.session.delete(claim)
        db.session.commit()
        return jsonify({"message":"Claim successfully deleted","data":data})
    except Exception as e:
        db.session.rollback()
        return {"message": "Error occurred","Error": str(e)}, 500


@claims_bp.post("/")
def add_claim():
    data = request.json
    new_claim= Claim(**data)
    try:
        db.session.add(new_claim)
        db.session.commit()
        result = {"message": "Claim added successfully", "data": new_claim.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return {"message": "Error occurred","Error": str(e)}, 500