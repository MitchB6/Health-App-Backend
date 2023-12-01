from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class Chatmessage(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    user = db.Column(db.String(225))
    message = db.Column(db.String(225))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(255))
    chatmessage = db.relationship('Chatmessage')