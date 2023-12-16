from datetime import datetime

from ..extensions import db

# The `MemberGoals` class represents a table in a database that stores goals for members, with methods
# for saving, deleting, and finding goals, as well as a property to check if a goal's deadline has
# passed.


class MemberGoals(db.Model):
  __tablename__ = 'member_goals'

  member_goal_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  goal_description = db.Column(db.Text, nullable=False)
  goal_type = db.Column(db.String(50), nullable=False)
  is_completed = db.Column(db.Boolean, nullable=False, default=False)
  date_completed = db.Column(db.Date, nullable=True)
  date_created = db.Column(db.Date, nullable=False,
                           default=datetime.utcnow().date())
  last_updated = db.Column(db.Date, nullable=False, default=datetime.utcnow().date(),
                           onupdate=datetime.utcnow().date())

  member = db.relationship('Member', back_populates='goals')

  def serialize(self):
    """Return object data in easily serializeable format."""
    return {
        'member_goal_id': self.member_goal_id,
        'member_id': self.member_id,
        'goal_description': self.goal_description,
        'goal_type': self.goal_type,
        'is_completed': self.is_completed,
        'date_completed': self.date_completed.strftime('%Y-%m-%d') if self.date_completed else None,
        'date_created': self.date_created.strftime('%Y-%m-%d') if self.date_created else None,
        'last_updated': self.last_updated.strftime('%Y-%m-%d') if self.last_updated else None,
    }

  def save(self, commit=True):
    """Save or update a member goal."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Delete a member goal."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_member(cls, member_id):
    """Find all goals for a specific member."""
    return cls.query.filter_by(member_id=member_id).all()

  @property
  def is_goal_deadline_passed(self):
    """Check if the goal deadline has passed."""
    return self.target_date < datetime.date.today()
