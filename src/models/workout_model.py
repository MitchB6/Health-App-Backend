from ..extensions import db
from .workoutplanlink_model import WorkoutPlanLink

# The `Workout` class represents a workout entity in a database, with various attributes and methods
# for saving, deleting, and linking workouts to workout plans.


class Workout(db.Model):
  __tablename__ = 'workouts'

  workout_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  workout_name = db.Column(db.String(255), nullable=False)
  workout_date = db.Column(db.Date, nullable=False)
  energy_level = db.Column(db.Integer)

  member = db.relationship('Member', back_populates='workouts')
  workout_plan_links = db.relationship(
      'WorkoutPlanLink', back_populates='workout', order_by='WorkoutPlanLink.sequence')
  workout_stats = db.relationship(
      'WorkoutStat', back_populates='workout', order_by='WorkoutStat.date')
  workout_exercises = db.relationship(
      'WorkoutExercise', back_populates='workout')

  def save(self, commit=True):
    """Save or update a workout."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Delete a workout."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_member(cls, member_id):
    """Find all workouts for a specific member."""
    return cls.query.filter_by(member_id=member_id).all()

  def link_to_workout_plan(self, plan_id, sequence, commit=True):
    """Link workout to a workout plan."""
    link = WorkoutPlanLink(workout_id=self.workout_id,
                           plan_id=plan_id, sequence=sequence)
    db.session.add(link)
    if commit:
      db.session.commit()

  def unlink_from_workout_plan(self, plan_id, commit=True):
    """Unlink workout from a workout plan."""
    link = WorkoutPlanLink.query.filter_by(
        workout_id=self.workout_id, plan_id=plan_id).first()
    if link:
      db.session.delete(link)
      if commit:
        db.session.commit()
