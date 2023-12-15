from ..extensions import db

class Chats(db.Model):
    __tablename__ = 'chatHistory'
    id = db.Column(db.Integer, primary_key=True)
    chatkey = db.Column(db.String(100))
    message = db.Column(db.Text)
