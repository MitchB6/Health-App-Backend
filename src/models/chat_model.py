from ..extensions import db

class Chats(db.Model):
    __tablename__ = 'chat_history_model'
    id = db.Column(db.Integer, primary_key=True)
    chatkey = db.Column(db.String(100))
    message = db.Column(db.Text)
    sender = db.Column(db.Integer, db.ForeignKey(
      'members.member_id'), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey(
      'members.member_id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    sender_member = db.relationship(
      'Member', foreign_keys=[sender])
    recipient_member = db.relationship(
      'Member', foreign_keys=[recipient])
    # Relationships (example: assuming a User table exists)
    # sender_user = db.relationship('User', foreign_keys=[sender])
    # recipient_user = db.relationship('User', foreign_keys=[recipient])

    def serialize(self):
        return {
            "id": self.id,
            "chatkey": self.chatkey,
            "message": self.message,
            "sender": self.sender,
            "recipient": self.recipient,
            "timestamp": self.timestamp.isoformat(),  # Convert to ISO format string
        } 