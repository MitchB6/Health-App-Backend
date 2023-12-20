from ..extensions import db
from ..models.workout_model import Workout

# The `WorkoutPlanLink` class represents a link between a workout plan and a workout in a database,
# with methods for saving, deleting, and finding links.


class WorkoutPlanLink(db.Model):
  __tablename__ = 'workout_plan_links'

  link_id = db.Column(db.Integer, primary_key=True)
  plan_id = db.Column(db.Integer, db.ForeignKey(
      'workout_plans.plan_id', ondelete='CASCADE'), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey(
      'workouts.workout_id'), nullable=False)
  workout_plan = db.relationship(
      'WorkoutPlan', back_populates='workout_plan_links')
  workout = db.relationship('Workout', back_populates='workout_plan_links')

  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'link_id': self.link_id,
        'plan_id': self.plan_id,
        'workout_id': self.workout_id,
    }

  def serialize_workout_in_plan(self):
    workout_info = Workout.query.filter_by(
        workout_id=self.workout_id).first()
    return {
        "link_id": self.link_id,
        "plan_id": self.plan_id,
        "workout_id": self.workout_id,
        'workout_name': workout_info.workout_name,
        'created_at': workout_info.created_at.last_modified.strftime('%Y-%m-%d') if workout_info.created_at else None,
        'last_modified': workout_info.last_modified.strftime('%Y-%m-%d') if workout_info.last_modified else None,
    }

  def save(self):
    """Saves a workout plan link to the database."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes a workout plan link from the database."""
    db.session.delete(self)
    db.session.commit()
