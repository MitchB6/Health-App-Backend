from ..extensions import db

# The `Availability` class represents the availability of a coach and provides methods for saving,
# deleting, and finding availabilities, as well as checking for overlapping availabilities.


class Availability(db.Model):
  __tablename__ = 'availability'

  availability_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey(
      'coach_info.coach_id', ondelete='CASCADE'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)

  coaches = db.relationship('CoachInfo', back_populates='availabilities')

  def save(self):
    """Save or update availability."""
    self.check_availability_overlap()
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Delete availability."""
    db.session.delete(self)
    db.session.commit()
