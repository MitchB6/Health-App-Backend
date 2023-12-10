from ..extensions import db

# The `WorkoutPlanLink` class represents a link between a workout plan and a workout in a database,
# with methods for saving, deleting, and finding links.


class WorkoutPlanLink(db.Model):
  __tablename__ = 'workout_plan_links'

  link_id = db.Column(db.Integer, primary_key=True)
  plan_id = db.Column(db.Integer, db.ForeignKey(
      'workout_plans.plan_id', ondelete='CASCADE'), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey(
      'workouts.workout_id'), nullable=False)
  sequence = db.Column(db.Integer, nullable=False)

  workout_plan = db.relationship(
      'WorkoutPlan', back_populates='workout_plan_links')
  workout = db.relationship('Workout', back_populates='workout_plan_links')

  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'link_id': self.link_id,
        'plan_id': self.plan_id,
        'workout_id': self.workout_id,
        'sequence': self.sequence
    }

  def save(self):
    """Saves a workout plan link to the database."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes a workout plan link from the database."""
    db.session.delete(self)
    db.session.commit()
