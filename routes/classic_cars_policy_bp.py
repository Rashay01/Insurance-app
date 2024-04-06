from flask import Blueprint, request, render_template, redirect, flash
from sqlalchemy.sql import func, Select
from models.classic_cars import ClassicCars
from models.policy import Policy
from extensions import db
from app import lg_user

classic_cars_policy_bp = Blueprint("classic_cars_policy", __name__)

@classic_cars_policy_bp.route("/")
def all_policies():
    data = Select(Policy,ClassicCars).join(ClassicCars,Policy.policy_number ==ClassicCars.policy_number).filter_by(customer_id=lg_user["ID"]).order_by(Policy.active.desc(), Policy.policy_date.desc())
    filtered_policies = db.session.execute(data).fetchall()
    if(len(filtered_policies)==0):
        return "<h2>You have no policies</h2>"
    all_policies_data = {
        "classic_car": filtered_policies
    } 
    return render_template("all-polices.html", curr_page="all policies", all_policies_data=all_policies_data)

@classic_cars_policy_bp.route("/<id>")
def specific_policies(id):
    data = Select(Policy,ClassicCars).join(ClassicCars,Policy.policy_number ==ClassicCars.policy_number).filter_by(customer_id=lg_user["ID"]).filter(Policy.policy_number==id).order_by(Policy.policy_date.desc())
    filtered_policies = db.session.execute(data).first()
    if filtered_policies is None:
        return "<h2>404 Policy not found</h2>"

    return render_template(
            "policy.html", curr_page="all polices", policy=filtered_policies[0], item=filtered_policies[1]
        )


@classic_cars_policy_bp.route("/delete", methods=["POST"])
def delete_user_specific_policies():
    policy_number = request.form.get('policy_number')
    try:
        policy = Policy.query.get(policy_number)
        if policy is None:
            return "<h2>404 Policy not found</h2>"
        policy.policy_end_date = func.now()
        policy.active = False
        db.session.commit()
        return redirect('/all-policies/')
    except Exception as e:
        db.session.rollback()
        return "<h2>500 Server Error</h2>"