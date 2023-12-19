from ..extensions import db

# The `WorkoutPlan` class represents a workout plan in a database, with methods for saving, deleting,
# linking and unlinking workouts, and retrieving linked workouts.


class WorkoutPlan(db.Model):
  __tablename__ = 'workout_plans'

  plan_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  plan_name = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=True)
  start_date = db.Column(db.Date, nullable=True)
  end_date = db.Column(db.Date, nullable=True)

  member = db.relationship('Member', back_populates='workout_plans')
  workout_plan_links = db.relationship(
      'WorkoutPlanLink', back_populates='workout_plan')

  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'plan_id': self.plan_id,
        'member_id': self.member_id,
        'plan_name': self.plan_name,
        'description': self.description,
        'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
        'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None
    }

  def create(self):
    """Create a new workout plan."""
    db.session.add(self)
    db.session.commit()

  def save(self):
    """Save changes to workout plan."""
    db.session.commit()

  def delete(self):
    """Delete a workout plan."""
    db.session.delete(self)
    db.session.commit()
