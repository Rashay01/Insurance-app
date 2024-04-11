from flask import Blueprint, render_template, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, ValidationError
from wtforms.validators import InputRequired, Length, Regexp
from sqlalchemy.sql import Select
from models.policy import Policy
from models.classic_cars import ClassicCars
from models.claim import Claim
from models.claim_status import ClaimStatus
from datetime import datetime, timedelta
from extensions import db
from app import lg_user
import uuid

all_claims_bp = Blueprint("all_claims", __name__)


class ClaimForm(FlaskForm):
    date_incident_occurred = DateField(
        "Date incident occurred", validators=[InputRequired()]
    )
    claim_description = TextAreaField(
        "Description of what happened?", validators=[InputRequired(), Length(max=500)]
    )
    police_claim_number = StringField(
        "Police claim number",
        validators=[
            InputRequired(),
            Length(max=15),
            Regexp("^[A-Za-z0-9_-]+$", message="Enter a valid police number"),
        ],
    )
    submit = SubmitField("Submit new claim")

    def validate_date_incident_occurred(self, field):
        curr_date = datetime.now().date()
        incident_date = field.data
        if incident_date > curr_date or curr_date - incident_date > timedelta(days=2):
            raise ValidationError("Claim must happen within two days of incident")


@all_claims_bp.route("/new-claim", methods=["POST", "GET"])
def new_claim():
    form = ClaimForm()
    polices_sql = (
        Select(Policy, ClassicCars)
        .join(ClassicCars, Policy.policy_number == ClassicCars.policy_number)
        .filter_by(customer_id=lg_user["ID"])
        .filter(Policy.active == True)
        .order_by(Policy.policy_number)
    )
    polices = db.session.execute(polices_sql).fetchall()
    if len(polices) == 0:
        return render_template(
            "Error-message.html",
            lg_user=lg_user,
            message="You have not taken a Policy out.",
            error_options="policy",
        )
    if form.validate_on_submit():
        claim_number = str(uuid.uuid4())
        policy_number = request.form.get("policy_number")
        data = {
            "claim_number": claim_number,
            "date_incident_occurred": form.date_incident_occurred.data.strftime(
                "%Y-%m-%d"
            ),
            "claim_description": form.claim_description.data,
            "police_claim_number": form.police_claim_number.data,
            "policy_number": policy_number,
        }
        status_data = {"status_name": "Received", "claim_number": claim_number}
        try:
            claim = Claim(**data)
            status = ClaimStatus(**status_data)
            db.session.add(claim)
            db.session.commit()
            db.session.add(status)
            db.session.commit()
            flash("New claim requested successfully")
            return redirect("/dashboard")
        except Exception as e:
            db.session.rollback()
            return render_template(
                "Error-message.html",
                lg_user=lg_user,
                message="Server Error",
                status_code="500",
                error_options=None,
            )

    return render_template(
        "new-claim.html", polices=polices, form=form, lg_user=lg_user
    )


@all_claims_bp.route("/all-claims")
def all_claims_page():
    claims_sql = (
        Select(Claim, Policy, ClassicCars)
        .join(Policy, Claim.policy_number == Policy.policy_number)
        .join(ClassicCars, Policy.policy_number == ClassicCars.policy_number)
        .filter_by(customer_id=lg_user["ID"])
        .order_by(Claim.claim_date.desc())
    )
    claims_Data = db.session.execute(claims_sql).fetchall()
    if len(claims_Data) == 0:
        return render_template(
            "Error-message.html",
            lg_user=lg_user,
            message="No claims have been made.",
            error_options="claim",
        )
    return render_template("all-claims.html", claims_data=claims_Data, lg_user=lg_user)


@all_claims_bp.route("/all-claims/<id>")
def specific_claims_page(id):
    claims_sql = (
        Select(Claim, Policy, ClassicCars)
        .join(Policy, Claim.policy_number == Policy.policy_number)
        .join(ClassicCars, Policy.policy_number == ClassicCars.policy_number)
        .filter_by(customer_id=lg_user["ID"])
        .filter(Claim.claim_number == id)
        .order_by(Claim.claim_date.desc())
    )
    claims_Data = db.session.execute(claims_sql).first()
    if claims_Data is None:
        return render_template(
            "Error-message.html",
            lg_user=lg_user,
            message="Claim not found",
            status_code="404",
            error_options=None,
        )
    status = (
        ClaimStatus.query.filter_by(claim_number=id)
        .order_by(ClaimStatus.status_date)
        .all()
    )

    return render_template(
        "claim.html",
        claim=claims_Data[0],
        quote=claims_Data[1],
        classic_car=claims_Data[2],
        statuses=status,
        lg_user=lg_user,
    )
