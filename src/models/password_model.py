from datetime import datetime

from ..extensions import db

# The `Password` class represents a table in a database that stores password information for members,
# including hashed passwords, creation and update timestamps, password reset tokens, and expiration
# dates.
class Password(db.Model):
  __tablename__ = 'passwords'
  
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), primary_key=True)
  hashed_pw = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  password_reset_token = db.Column(db.String(64), nullable=True)
  password_reset_expiration = db.Column(db.DateTime, nullable=True)

  member = db.relationship("Member", back_populates="passwords")
  
  def __init__(self, **kwargs):
    """Initialize a Password instance."""
    super().__init__(**kwargs)
    
  def save(self):
    """Saves the Password instance to the DB."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes the Password instance from the DB."""
    db.session.delete(self)
    db.session.commit()