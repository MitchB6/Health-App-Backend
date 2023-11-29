from ..extensions import db

class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    birthdate = db.Column(db.Date)
    height = db.Column(db.Integer)  
    weight = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    member = db.relationship('Member', back_populates='personal_info')
