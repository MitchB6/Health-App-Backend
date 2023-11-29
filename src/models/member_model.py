from datetime import datetime
from ..extensions import db

# The `Member` class represents a member in a database, with various attributes and relationships to
# other tables.
class Member(db.Model):
  __tablename__ = 'members'

  member_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), nullable=True)
  first_name = db.Column(db.String(100), nullable=True)
  last_name = db.Column(db.String(100), nullable=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  phone = db.Column(db.String(20), nullable=True)
  role_id = db.Column(db.Boolean, nullable=False, default=False)
  city = db.Column(db.String(100), nullable=True)
  state = db.Column(db.String(100), nullable=True)
  zip_code = db.Column(db.String(20), nullable=True)
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  birthdate = db.Column(db.Date, nullable=True)
  height = db.Column(db.Integer, nullable=True)  
  weight = db.Column(db.Integer, nullable=True)

  passwords = db.relationship('Password', back_populates='member', uselist=False)
  coaches = db.relationship('CoachInfo', secondary='coaches_members_link', back_populates='member')
  coach_info = db.relationship('CoachInfo', back_populates='member')
  goals = db.relationship('MemberGoals', back_populates='member')
  workouts = db.relationship('Workout', back_populates='member')
  workout_plans = db.relationship('WorkoutPlan', back_populates='member')

  def __repr__(self):
    """String representation of a Member instance."""
    return f"<Member {self.first_name} {self.last_name}>"

  def save(self, flush=False, commit=False):
    """Saves the Member instance. Use 'flush' to get member_id without committing"""
    db.session.add(self)
    if flush:
      db.session.flush()
    if commit:
      db.session.commit()
  
  def delete(self):
    """ Permanently delete the member """
    db.session.delete(self)
    db.session.commit()
    
  def update(self, **kwargs):
    """Updates Member attributes specified in 'kwargs'."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()