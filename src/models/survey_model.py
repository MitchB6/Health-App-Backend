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
  recorded_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow().date())

  member = db.relationship('Member', back_populates='surveys')

  def serialize(self):
    return {
        'survey_id': self.survey_id,
        'member_id': self.member_id,
        'date': self.date,
        'mood_level': self.mood_level,
        'hydration_level': self.hydration_level,
        'calories_intake': self.calories_intake,
        'recorded_at': self.recorded_at
    }

  def save(self):
    """Save or update a workout."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Delete a workout."""
    db.session.delete(self)
    db.session.commit()
