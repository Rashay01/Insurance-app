from extensions import db

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_desc = db.Column(db.String(500))
    premium_percentage = db.Column(db.Float, nullable= False)

    def to_dict(self):
        return{
            "category_id":self.category_id,
            "category_name":self.category_name,
            "category_desc":self.category_desc,
            "premium_percentage":self.premium_percentage,
        }