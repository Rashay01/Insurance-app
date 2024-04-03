from flask import Blueprint, jsonify, request
from models.quote import Quote
from extensions import db

quotes_bp = Blueprint("quotes", __name__)


@quotes_bp.get("/")
def get_quote():
    quotes_list = Quote.query.all()
    data = [
        quote.to_dict() for quote in quotes_list
    ] 
    return jsonify(data)


@quotes_bp.get("/<id>")
def get_specific_quote(id):
    quotes_list = Quote.query.get(id)
    if quotes_list is None:
        return jsonify({"message": "Quote Not found"}), 404
    return jsonify(quotes_list.to_dict())


@quotes_bp.delete("/<id>")
def delete_specific_quote(id):
    quote = Quote.query.get(id)
    if quote is None:
        return jsonify({"message": "Quote Not found"}), 404
    try:
        data = quote.to_dict()
        db.session.delete(quote)
        db.session.commit()
        return jsonify({"message":"Quote successfully deleted","data":data})
    except Exception as e:
        db.session.rollback()  
        return {"message": "Error occurred","Error": str(e)}, 500

@quotes_bp.post("/")
def update_the_quote():
    data = request.json
    new_quote= Quote(**data)
    try:
        db.session.add(new_quote)
        db.session.commit()
        result = {"message": "User added successfully", "data": new_quote.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        return {"message": "Error occurred","Error": str(e)}, 500

@quotes_bp.put("/<id>")
def update_specific_quote(id):
    quote_update = request.json
    quote = Quote.query.get(id)
    if quote is None:
        return jsonify({"message": "Quote Not found"}), 404
    try:
        for key, value in quote_update.items():
            if hasattr(quote, key):
                setattr(quote, key, value)
        db.session.commit()
        result = {"message": "Quote updated successfully", "data": quote.to_dict()}
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return {"message": "Error occurred","Error": str(e)}, 500