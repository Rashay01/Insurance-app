from flask import Blueprint, request, render_template, redirect, flash
from sqlalchemy.sql import func, Select
from models.classic_cars import ClassicCars
from flask_login import current_user, login_required
from models.policy import Policy
from extensions import db


classic_cars_policy_bp = Blueprint("classic_cars_policy", __name__)

#DIsplays all the policies with classic cars 
@classic_cars_policy_bp.route("/")
@login_required
def all_policies():
    data = (
        Select(Policy, ClassicCars)
        .join(ClassicCars, Policy.policy_number == ClassicCars.policy_number)
        .filter_by(customer_id=current_user.ID)
        .order_by(Policy.active.desc(), Policy.policy_date.desc())
    )
    filtered_policies = db.session.execute(data).fetchall()
    if len(filtered_policies) == 0:
        return render_template(
            "Error-message.html",
            message="You have not taken a policy out.",
            error_options="policy",
        )
    all_policies_data = {"classic_car": filtered_policies}
    return render_template(
        "all-polices.html",
        curr_page="all policies",
        all_policies_data=all_policies_data,
    )


# Displays a single policy 
@classic_cars_policy_bp.route("/<id>")
@login_required
def specific_policies(id):
    data = (
        Select(Policy, ClassicCars)
        .join(ClassicCars, Policy.policy_number == ClassicCars.policy_number)
        .filter_by(customer_id=current_user.ID)
        .filter(Policy.policy_number == id)
        .order_by(Policy.policy_date.desc())
    )
    filtered_policies = db.session.execute(data).first()
    if filtered_policies is None:
        return render_template(
            "Error-message.html",
            message="Policy not found",
            status_code="404",
            error_options=None,
        )

    return render_template(
        "policy.html",
        curr_page="all polices",
        policy=filtered_policies[0],
        item=filtered_policies[1],
    )

# Delete a policy
@classic_cars_policy_bp.route("/delete", methods=["POST"])
@login_required
def delete_user_specific_policies():
    policy_number = request.form.get("policy_number")
    try:
        policy = Policy.query.get(policy_number)
        if policy is None:
            return render_template(
                "Error-message.html",
                message="Policy not found",
                status_code="404",
                error_options=None,
            )
        policy.policy_end_date = func.now()
        policy.active = False
        db.session.commit()
        flash("Policy removed")
        return redirect("/all-policies/")
    except Exception as e:
        db.session.rollback()
        return render_template(
            "Error-message.html",
            message="Server Error",
            status_code="500",
            error_options=None,
        )
