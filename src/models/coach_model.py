from ..models.personalinfo_model import PersonalInfo
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
  schedule_general = db.Column(db.Text)
  qualifications = db.Column(db.Text)
  approved = db.Column(db.Boolean, default=False)

  member = db.relationship('Member', back_populates='coaches')
  availabilities = db.relationship('Availability', back_populates='coaches',
                                   order_by='Availability.start_time', cascade='all, delete-orphan')
  members = db.relationship(
      'Member', secondary='coaches_members_link', back_populates='coaches')

  def serialize(self):
    personal_info = PersonalInfo.query.filter_by(
        member_id=self.member_id).first()
    return {
        'coach_id': self.coach_id,
        'member_id': self.member_id,
        'first_name': personal_info.first_name if personal_info else None,
        'last_name': personal_info.last_name if personal_info else None,
        'specialization': self.specialization,
        'price': float(self.price),
        'location': self.location,
        'schedule_general': self.schedule_general,
        'qualifications': self.qualifications,
        'approved': self.approved
    }

  def save(self):
    """Saves coach information to the database."""
    db.session.add(self)
    db.session.commit()

  def update(self, **kwargs):
    """Updates coach attributes with given keyword arguments."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
