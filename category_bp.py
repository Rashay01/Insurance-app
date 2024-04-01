from flask import Blueprint, jsonify, request
from app import Category,db

category_bp = Blueprint("category", __name__)

@category_bp.get("/")
def get_category():
    category_list = Category.query.all()
    data = [
        category.to_dict() for category in category_list
    ] 
    return jsonify(data)

@category_bp.get("/<id>")
def get_specific_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({"message": "Category Not found"}), 404
    return jsonify(category.to_dict())

@category_bp.put("/<id>")
def update_specific_category(id):
    category_update = request.json
    category = Category.query.get(id)
    if category is None:
        return jsonify({"message": "Category Not found"}), 404
    try:
        for key, value in category_update.items():
            if hasattr(category, key):
                setattr(category, key, value)
        db.session.commit()
        result = {"message": "category updated successfully", "data": category.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500
    
@category_bp.delete("/<id>")
def delete_specific_category(id):
    category = Category.query.get(id)
    if category is None:
        return jsonify({"message": "category Not found"}), 404
    try:
        data = category.to_dict()
        db.session.delete(category)
        db.session.commit()
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500
    
@category_bp.post("/")
def add_category():
    data = request.json
    new_category= Category(**data)
    try:
        db.session.add(new_category)
        db.session.commit()
        result = {"message": "Category added successfully", "data": new_category.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500