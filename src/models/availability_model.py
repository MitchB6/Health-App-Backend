from ..extensions import db

# The `Availability` class represents the availability of a coach and provides methods for saving,
# deleting, and finding availabilities, as well as checking for overlapping availabilities.
class Availability(db.Model):
  __tablename__ = 'availability'

  availability_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)

  coach_info = relationship('CoachInfo', back_populates='availabilities')
  
  def save(self):
    """Save or update availability."""
    self.check_availability_overlap()
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Delete availability."""
    db.session.delete(self)
    db.session.commit()
  
  @classmethod
  def find_by_coach(cls, coach_id):
    """Find all availabilities for a specific coach."""
    return cls.query.filter_by(coach_id=coach_id).all()

  def check_availability_overlap(self):
    """Check for overlapping availability."""
    overlapping = Availability.query.filter(
      Availability.coach_id == self.coach_id,
      Availability.start_time < self.end_time,
      Availability.end_time > self.start_time
    ).first()
    if overlapping and overlapping.availability_id != self.availability_id:
      raise ValueError("This time slot overlaps with an existing availability.")