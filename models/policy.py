from sqlalchemy.sql import func
from extensions import db
import uuid


class Policy(db.Model):
    __tablename__ = "policy"
    policy_number = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    policy_date = db.Column(db.DateTime, nullable=False, default=func.current_date())
    monthly_premium = db.Column(db.Float, nullable=False)
    policy_end_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, nullable=False, default=True)
    category_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "policy_number": self.policy_number,
            "policy_date": self.policy_date,
            "monthly_premium": self.monthly_premium,
            "policy_end_date": self.policy_end_date,
            "active": self.active,
            "category_id": self.category_id,
        }
