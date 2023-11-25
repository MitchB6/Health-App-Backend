from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class Note(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(150), unique=True)
    frist_name = db.Column(db.String(150))
    password = db.Column(db.String(255))
    notes = db.relationship('Note')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attrabute')
    
    @password.setter
    def mpassword(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_pasword(self, password):
        return check_password_hash(self.password_hash, password)

    def check_password(self, password):
        self.password = check_password_hash(self.password,password)