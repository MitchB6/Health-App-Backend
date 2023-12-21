from datetime import datetime

from ..extensions import db

# The `Workout` class represents a workout entity in a database, with various attributes and methods
# for saving, deleting, and linking workouts to workout plans.


class Workout(db.Model):
  __tablename__ = 'workouts'

  workout_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  workout_name = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.Date, nullable=False, default=datetime.utcnow)
  last_modified = db.Column(db.Date, nullable=False, default=datetime.utcnow)

  member = db.relationship('Member', back_populates='workouts')
  workout_plan_links = db.relationship(
      'WorkoutPlanLink', back_populates='workout')
  workout_stats = db.relationship(
      'WorkoutStat', back_populates='workout', order_by='WorkoutStat.date')
  workout_exercises = db.relationship(
      'WorkoutExercise', back_populates='workout')

  def serialize(self):
    return {
        'workout_id': self.workout_id,
        'member_id': self.member_id,
        'workout_name': self.workout_name,
        'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
        'last_modified': self.last_modified.strftime('%Y-%m-%d') if self.last_modified else None,
    }

  def save(self):
    """Save or update a workout."""
    db.session.add(self)
    db.session.flush()
    db.session.commit()

  def delete(self):
    """Delete a workout."""
    db.session.delete(self)
    db.session.commit()
