from datetime import datetime
from ..extensions import db

# The `Member` class represents a member in a database, with various attributes and relationships to
# other tables.


class Member(db.Model):
  __tablename__ = 'members'

  member_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), nullable=True, unique=True)
  role_id = db.Column(db.Integer, nullable=False, default=0)
  join_date = db.Column(db.Date, nullable=False,
                        default=datetime.utcnow().date())

  personal_info = db.relationship(
      'PersonalInfo', back_populates='member', uselist=False, cascade='all, delete-orphan')
  passwords = db.relationship(
      'Password', back_populates='member', uselist=False, cascade='all, delete-orphan')
  coaches = db.relationship(
      'CoachInfo', secondary='coaches_members_link', back_populates='member')
  goals = db.relationship(
      'MemberGoals', back_populates='member', cascade='all, delete-orphan')
  workouts = db.relationship(
      'Workout', back_populates='member', cascade='all, delete-orphan')
  workout_plans = db.relationship(
      'WorkoutPlan', back_populates='member', cascade='all, delete-orphan')
  surveys = db.relationship(
      'Survey', back_populates='member', cascade='all, delete-orphan')
  sent_chats = db.relationship('Chats', foreign_keys='Chats.sender',
                               backref='sender_member', lazy='dynamic')
  received_chats = db.relationship('Chats', foreign_keys='Chats.recipient',
                                   backref='recipient_member', lazy='dynamic')

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
