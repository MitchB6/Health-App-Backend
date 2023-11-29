from ..extensions import db
from .workoutplanlink_model import WorkoutPlanLink

# The `WorkoutPlan` class represents a workout plan in a database, with methods for saving, deleting,
# linking and unlinking workouts, and retrieving linked workouts.
class WorkoutPlan(db.Model):
  __tablename__ = 'workout_plans'

  plan_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  plan_name = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=True)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=True)

  member = db.relationship('Member', back_populates='workout_plans')
  workout_plan_links = db.relationship('WorkoutPlanLink', back_populates='workout_plan', order_by='WorkoutPlanLink.sequence')

  def save(self, commit=True):
    """Save or update a workout plan."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Delete a workout plan."""
    db.session.delete(self)
    db.session.commit()

  def link_workout(self, workout_id, sequence, commit=True):
    """Link a workout to this workout plan."""
    link = WorkoutPlanLink(plan_id=self.plan_id, workout_id=workout_id, sequence=sequence)
    db.session.add(link)
    if commit:
      db.session.commit()

  def unlink_workout(self, workout_id, commit=True):
    """Unlink a workout from this workout plan."""
    link = WorkoutPlanLink.query.filter_by(plan_id=self.plan_id, workout_id=workout_id).first()
    if link:
      db.session.delete(link)
      if commit:
        db.session.commit()

  def get_workouts(self):
    """Retrieve all workouts linked to this workout plan."""
    return [link.workout for link in self.workout_plan_links]