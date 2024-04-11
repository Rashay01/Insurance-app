from flask import Blueprint, jsonify, request
from models.cars_quote import CarQuote
from extensions import db

cars_quote_bp = Blueprint("cars_quote", __name__)


@cars_quote_bp.get("/")
def get_cars_quote():
    cars_quote_list = CarQuote.query.all()
    data = [cars_quote.to_dict() for cars_quote in cars_quote_list]
    return jsonify(data)


@cars_quote_bp.get("/<vehicleId>/<quoteId>")
def get_specific_cars_quote(vehicleId, quoteId):
    cars_quote = CarQuote.query.get({"vehicle_id": vehicleId, "quote_id": quoteId})
    if cars_quote is None:
        return jsonify({"message": "Cars Quote link Not found"}), 404
    return jsonify(cars_quote.to_dict())


@cars_quote_bp.put("/<vehicleId>/<quoteId>")
def update_specific_cars_quote(vehicleId, quoteId):
    cars_quote_update = request.json
    cars_quote = CarQuote.query.get({"vehicle_id": vehicleId, "quote_id": quoteId})
    if cars_quote is None:
        return jsonify({"message": "Cars Quote link Not found"}), 404
    try:
        for key, value in cars_quote_update.items():
            if hasattr(cars_quote, key):
                setattr(cars_quote, key, value)
        db.session.commit()
        result = {
            "message": "Cars Quote link updated successfully",
            "data": cars_quote.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@cars_quote_bp.delete("/<vehicleId>/<quoteId>")
def delete_specific_cars_quote(vehicleId, quoteId):
    cars_quote = CarQuote.query.get({"vehicle_id": vehicleId, "quote_id": quoteId})
    if cars_quote is None:
        return jsonify({"message": "Cars Quote link Not found"}), 404
    try:
        data = cars_quote.to_dict()
        db.session.delete(cars_quote)
        db.session.commit()
        return jsonify(
            {"message": "Cars Quote link successfully deleted", "data": data}
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@cars_quote_bp.post("/")
def add_cars_quote():
    data = request.json
    new_cars_quote = CarQuote(**data)
    try:
        db.session.add(new_cars_quote)
        db.session.commit()
        result = {
            "message": "Cars Quote link added successfully",
            "data": new_cars_quote.to_dict(),
        }
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500
