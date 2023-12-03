from ..extensions import db

# The CoachInfo class represents coach information in a database and provides methods for saving,
# deleting, updating, and retrieving coach data.


class CoachInfo(db.Model):
  __tablename__ = 'coach_info'

  coach_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  specialization = db.Column(db.Text)
  price = db.Column(db.Numeric(10, 2))
  location = db.Column(db.Text)
  schedule_text = db.Column(db.Text)
  qualifications = db.Column(db.Text)
  approved = db.Column(db.Boolean, default=False)

  member = db.relationship('Member', back_populates='coaches')
  availabilities = db.relationship('Availability', back_populates='coaches',
                                   order_by='Availability.start_time', cascade='all, delete-orphan')
  members = db.relationship(
      'Member', secondary='coaches_members_link', back_populates='coaches')

  def save(self, flush=False, commit=False):
    """Saves coach information to the database."""
    db.session.add(self)
    if flush:
      db.session.flush()
    if commit:
      db.session.commit()

  def delete(self):
    """Deletes coach information from the database."""
    db.session.delete(self)
    db.session.commit()

  def update(self, **kwargs):
    """Updates coach attributes with given keyword arguments."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()

  @classmethod
  def all_coaches(cls):
    """Returns all registered coaches."""
    return cls.query.all()
