from extensions import db
import uuid
from sqlalchemy.sql import func


class Quote(db.Model):
    __tablename__ = "quote"
    quote_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    quote_date = db.Column(db.DateTime, nullable=False, default=func.current_date())
    quoted_premium = db.Column(db.Float, nullable=False)
    quote_decision_date = db.Column(db.DateTime)
    status = db.Column(db.String(30), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "quote_id": self.quote_id,
            "quote_date": self.quote_date,
            "quoted_premium": self.quoted_premium,
            "quote_decision_date": self.quote_decision_date,
            "status": self.status,
            "category_id": self.category_id,
        }
