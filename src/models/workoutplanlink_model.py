from ..extensions import db

# The `WorkoutPlanLink` class represents a link between a workout plan and a workout in a database,
# with methods for saving, deleting, and finding links.
class WorkoutPlanLink(db.Model):
  __tablename__ = 'workout_plan_links'

  link_id = db.Column(db.Integer, primary_key=True)
  plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.plan_id'), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
  sequence = db.Column(db.Integer, nullable=False)

  workout_plan = db.relationship('WorkoutPlan', back_populates='workout_plan_links')
  workout = db.relationship('Workout', back_populates='workout_plan_links')

  def save(self, commit=False):
    """Saves a workout plan link to the database."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Deletes a workout plan link from the database."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_plan_id(cls, plan_id):
    """Finds all workout plan links for a given plan ID."""
    return cls.query.filter_by(plan_id=plan_id).all()

  @classmethod
  def find_by_workout_id(cls, workout_id):
    """Finds all workout plan links for a given workout ID."""
    return cls.query.filter_by(workout_id=workout_id).all()

  @classmethod
  def find_link(cls, plan_id, workout_id):
    """Finds a specific link between a workout plan and a workout."""
    return cls.query.filter_by(plan_id=plan_id, workout_id=workout_id).first()