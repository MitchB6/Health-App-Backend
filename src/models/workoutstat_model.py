from datetime import datetime
from ..extensions import db

# The `WorkoutStat` class represents a workout statistic and provides methods for saving, deleting,
# and finding workout stats in the database.


class WorkoutStat(db.Model):
  __tablename__ = 'workout_stats'

  stat_id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey(
      'workouts.workout_id', ondelete='CASCADE'), nullable=False)
  duration = db.Column(db.Integer)
  calories_burned = db.Column(db.Integer)
  date = db.Column(db.Date, default=datetime.utcnow().date())

  workout = db.relationship('Workout', back_populates='workout_stats')

  def serialize(self):
    return {
        'stat_id': self.stat_id,
        'workout_id': self.workout_id,
        'duration': self.duration,
        'calories_burned': self.calories_burned,
        'date': self.date.strftime('%Y-%m-%d') if self.date else None
    }

  def save(self):
    """Saves a workout statistic to the database."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes a workout statistic from the database."""
    db.session.delete(self)
    db.session.commit()
