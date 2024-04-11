from extensions import db
import uuid


class ClassicCars(db.Model):
    __tablename__ = "classic_cars"
    vehicle_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    vehicle_make = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    year_model = db.Column(db.String(4), nullable=False)
    vin = db.Column(db.String(20), nullable=False)
    license_plate_number = db.Column(db.String(10), nullable=False)
    odometer_reading = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(10))
    color = db.Column(db.String(20))
    policy_number = db.Column(db.String(50))
    customer_id = db.Column(db.String(50))
    current_value = db.Column(db.Float, nullable=False)
    year_purchased = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_make": self.vehicle_make,
            "model": self.model,
            "year_model": self.year_model,
            "vin": self.vin,
            "license_plate_number": self.license_plate_number,
            "odometer_reading": self.odometer_reading,
            "fuel_type": self.fuel_type,
            "color": self.color,
            "policy_number": self.policy_number,
            "customer_id": self.customer_id,
            "current_value": self.current_value,
            "year_purchased": self.year_purchased,
        }
