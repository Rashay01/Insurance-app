from flask import Blueprint, jsonify, request
from models.classic_cars import ClassicCars
from extensions import db

classic_car_bp = Blueprint("classic_car", __name__)


@classic_car_bp.get("/")
def get_classic_car():
    ClassicCars_list = ClassicCars.query.all()
    data = [car.to_dict() for car in ClassicCars_list]
    return jsonify(data)


@classic_car_bp.get("/<id>")
def get_specific_classic_car(id):
    cars_list = ClassicCars.query.get(id)
    if cars_list is None:
        return jsonify({"message": "Classic Car Not found"}), 404
    return jsonify(cars_list.to_dict())


@classic_car_bp.put("/<id>")
def update_specific_classic_car(id):
    car_update = request.json
    selected_car = ClassicCars.query.get(id)
    if selected_car is None:
        return jsonify({"message": "Classic Car Not found"}), 404
    try:
        for key, value in car_update.items():
            if hasattr(selected_car, key):
                setattr(selected_car, key, value)
        db.session.commit()
        result = {
            "message": "Classic Cars updated successfully",
            "data": selected_car.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@classic_car_bp.delete("/<id>")
def delete_specific_classic_car(id):
    selected_car = ClassicCars.query.get(id)
    if selected_car is None:
        return jsonify({"message": "Classic Cars Not found"}), 404
    try:
        data = selected_car.to_dict()
        db.session.delete(selected_car)
        db.session.commit()
        return jsonify({"message": "Classic Cars deleted successfully", "data": data})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500


@classic_car_bp.post("/")
def add_classic_car():
    data = request.json
    new_car = ClassicCars(**data)
    try:
        db.session.add(new_car)
        db.session.commit()
        result = {
            "message": "Classic Car added successfully",
            "data": new_car.to_dict(),
        }
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "Error occurred", "Error": str(e)}), 500
