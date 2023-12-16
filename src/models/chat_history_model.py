from ..extensions import db


class Chats(db.Model):
  __tablename__ = 'chatHistory'

  id = db.Column(db.Integer, primary_key=True)
  link_id = db.Column(db.Integer, db.ForeignKey(
      'coaches_members_link.link_id'), nullable=False)
  chatkey = db.Column(db.String(100))
  message = db.Column(db.Text)
  recorded_at = db.Column(db.Date, default=db.func.current_date())


def serialize(self):
  """Return object data in easily serializeable format."""
  return {
      'id': self.id,
      'chatkey': self.chatkey,
      'message': self.message,
      'recorded_at': self.recorded_at.strftime('%Y-%m-%d') if self.recorded_at else None
  }
