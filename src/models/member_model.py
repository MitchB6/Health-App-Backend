from datetime import datetime
from ..extensions import db

# The `Member` class represents a member in a database, with various attributes and relationships to
# other tables.
class Member(db.Model):
  __tablename__ = 'members'

  member_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), nullable=True)
  role_id = db.Column(db.Integer, nullable=False, default=False)
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  personal_info = db.relationship('PersonalInfo', back_populates='member', uselist=False)
  passwords = db.relationship('Password', back_populates='member', uselist=False)
  coaches = db.relationship('CoachInfo', secondary='coaches_members_link', back_populates='member')
  coach_info = db.relationship('CoachInfo', back_populates='member')
  goals = db.relationship('MemberGoals', back_populates='member')
  workouts = db.relationship('Workout', back_populates='member')
  workout_plans = db.relationship('WorkoutPlan', back_populates='member')

  def __repr__(self):
    """String representation of a Member instance."""
    if self.personal_info:
      return f"<Member {self.personal_info.first_name} {self.personal_info.last_name}>"
    return f"<Member {self.member_id}>"
  
  def delete(self):
    """ Permanently delete the member """
    db.session.delete(self)
    db.session.commit()
    
  def update(self, **kwargs):
    """Updates Member attributes specified in 'kwargs'."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
      elif hasattr(self.personal_info, key) and value is not None:
        setattr(self.personal_info, key, value)
    db.session.commit()