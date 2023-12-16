from datetime import datetime
from ..extensions import db

# The `ExerciseStat` class represents exercise statistics and provides methods for saving, deleting,
# updating, and finding exercise stats in the database.


class ExerciseStat(db.Model):
  __tablename__ = 'exercise_stats'

  stat_id = db.Column(db.Integer, primary_key=True)
  exercise_id = db.Column(db.Integer, db.ForeignKey(
      'exercises.exercise_id', ondelete='CASCADE'), nullable=False)
  set_number = db.Column(db.Integer)
  reps_completed = db.Column(db.Integer)
  weight = db.Column(db.Numeric(10, 2))
  duration = db.Column(db.Integer)
  recorded_at = db.Column(db.DateTime, default=datetime.utcnow().date())

  exercise = db.relationship('Exercise', back_populates='stats')

  def serialize(self):
    """Return object data in easily serializeable format."""
    return {
        'stat_id': self.stat_id,
        'exercise_id': self.exercise_id,
        'set_number': self.sets_completed,
        'reps_completed': self.reps_completed,
        'weight': float(self.weight),
        'duration': self.duration,
        'recorded_at': self.recorded_at.strftime('%Y-%m-%d') if self.recorded_at else None
    }

  def save(self):
    """Saves exercise stat to the database."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes exercise stat from the database."""
    db.session.delete(self)
    db.session.commit()

  def update(self, **kwargs):
    """Updates exercise stats with given keyword arguments."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()
