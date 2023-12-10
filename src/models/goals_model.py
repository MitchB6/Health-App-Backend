from datetime import datetime

from ..extensions import db

# The `MemberGoals` class represents a table in a database that stores goals for members, with methods
# for saving, deleting, and finding goals, as well as a property to check if a goal's deadline has
# passed.
class MemberGoals(db.Model):
  __tablename__ = 'member_goals'

  member_goal_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
  goal_description = db.Column(db.Text, nullable=False)
  target_date = db.Column(db.Date, nullable=False)
  goal_type = db.Column(db.String(50), nullable=False)

  member = db.relationship('Member', back_populates='goals')
  
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