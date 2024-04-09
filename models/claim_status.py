from sqlalchemy.sql import func
from extensions import db
import uuid


class ClaimStatus(db.Model):
    __tablename__ = "claim_status"
    status_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    status_name = db.Column(db.String(20), nullable=False)
    status_date = db.Column(db.DateTime, nullable=False, default=func.current_date())
    claim_number = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "status_id": self.status_id,
            "status_name": self.status_name,
            "status_date": self.status_date,
            "claim_number": self.claim_number,
        }
