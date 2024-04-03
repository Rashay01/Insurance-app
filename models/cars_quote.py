from sqlalchemy.sql import func
from extensions import db
import uuid

class CarQuote(db.Model):
    __tablename__ = "car_quote"
    vehicle_id = db.Column(db.String(50))
    quote_id = db.Column(db.String(50))

    def to_dict(self):
        return{
            "vehicle_id":self.vehicle_id,
            "quote_id":self.quote_id,
        }