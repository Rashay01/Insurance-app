from extensions import db

class User(db.Model):
    __tablename__ = "users"
    ID = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)  
    surname = db.Column(db.String(50), nullable=False)  
    email = db.Column(db.String(50), nullable=False)  
    cell_no = db.Column(db.String(50), nullable=False)  
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200))

    # JSON - Keys
    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "cell_no":self.cell_no,
            "password": self.password,
            "address":self.address
        }