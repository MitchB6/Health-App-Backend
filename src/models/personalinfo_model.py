from ..extensions import db


class PersonalInfo(db.Model):
  __tablename__ = 'personal_info'

  id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  username = db.Column(db.String(255))
  phone = db.Column(db.String(20))
  city = db.Column(db.String(100))
  state = db.Column(db.String(100))
  zip_code = db.Column(db.String(20))
  birthdate = db.Column(db.Date)
  height = db.Column(db.Integer)
  weight = db.Column(db.Integer)
  age = db.Column(db.Integer)
  gender = db.Column(db.String(20))

  member = db.relationship(
      'Member', back_populates='personal_info', uselist=False)

  @classmethod
  def create(cls, **kwargs):
    """Creates a new PersonalInfo record and saves it to the database."""
    new_info = cls(**kwargs)
    db.session.add(new_info)
    db.session.commit()
    return new_info

  def update(self, **kwargs):
    """Updates existing PersonalInfo fields with new values."""
    for key, value in kwargs.items():
      if hasattr(self, key):
        setattr(self, key, value)
    db.session.commit()

  def delete(self):
    """Deletes the PersonalInfo record from the database."""
    db.session.delete(self)
    db.session.commit()
