from sqlalchemy.sql import func
from extensions import db
import uuid


class Claim(db.Model):
    __tablename__ = "claim"
    claim_number = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    claim_date = db.Column(db.DateTime, nullable=False, default=func.current_date())
    date_incident_occurred = db.Column(db.DateTime, nullable=False)
    claim_description = db.Column(db.String(500), nullable=False)
    police_claim_number = db.Column(db.String(15))
    claim_amount = db.Column(db.Float)
    policy_number = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "claim_number": self.claim_number,
            "claim_date": self.claim_date,
            "date_incident_occurred": self.date_incident_occurred,
            "claim_description": self.claim_description,
            "police_claim_number": self.police_claim_number,
            "claim_amount": self.claim_amount,
            "policy_number": self.policy_number,
        }
