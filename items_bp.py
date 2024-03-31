from flask import Blueprint, jsonify, request
from app import Item,db

items_bp = Blueprint("items", __name__)

@items_bp.get("/")
def get_items():
    items_list = Item.query.all()
    data = [
        item.to_dict() for item in items_list
    ] 
    return jsonify(data)


@items_bp.get("/<id>")
def get_specific_item(id):
    items_list = Item.query.get(id)
    if items_list is None:
        return jsonify({"message": "Item Not found"}), 404
    return jsonify(items_list.to_dict())


@items_bp.put("/<id>")
def update_specific_item(id):
    item_update = request.json
    selected_item = Item.query.get(id)
    if selected_item is None:
        return jsonify({"message": "Item Not found"}), 404
    try:
        for key, value in item_update.items():
            if hasattr(selected_item, key):
                setattr(selected_item, key, value)
        db.session.commit()
        result = {"message": "Item updated successfully", "data": selected_item.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500


@items_bp.delete("/<id>")
def delete_specific_item(id):
    selected_item = Item.query.get(id)
    if selected_item is None:
        return jsonify({"message": "Item Not found"}), 404
    try:
        data = selected_item.to_dict()
        db.session.delete(selected_item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully", "data": data})
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500


@items_bp.post("/")
def add_Item():
    data = request.json
    new_item= Item(**data)
    try:
        db.session.add(new_item)
        db.session.commit()
        result = {"message": "Item added successfully", "data": new_item.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500