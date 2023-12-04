from datetime import datetime
from ..extensions import db


class Survey(db.Model):
  __tablename__ = 'survey'

  survey_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  date = db.Column(db.DateTime, nullable=False)
  energy_level = db.Column(db.Integer)
  mood_level = db.Column(db.Integer)
  hydration_level = db.Column(db.Float)
  calories_intake = db.Column(db.Integer)
  recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  member = db.relationship('Member', back_populates='surveys')

  def __repr__(self):
    return f"<UserSurvey {self.user_id}>"
