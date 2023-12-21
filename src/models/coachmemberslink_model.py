from ..extensions import db
from .coach_model import CoachInfo
from .member_model import Member
from .personalinfo_model import PersonalInfo

# The `CoachesMembersLink` class is a model that represents the link between coaches and members in a
# database, providing methods to create, remove, and find links between them.


class CoachesMembersLink(db.Model):
  __tablename__ = 'coaches_members_link'

  link_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey(
      'coach_info.coach_id', ondelete='CASCADE'), nullable=False)
  member_id = db.Column(db.Integer, db.ForeignKey(
      'members.member_id', ondelete='CASCADE'), nullable=False)
  status = db.Column(db.String(20), nullable=False, default='pending')
  last_updated = db.Column(db.Date, nullable=False, default=db.func.current_date(
  ), onupdate=db.func.current_date())

  def serialize(self):
    client_info = PersonalInfo.query.filter_by(
        member_id=self.member_id).first()
    return {
        "link_id": self.link_id,
        "coach_id": self.coach_id,
        "member_id": self.member_id,
        "first_name": client_info.first_name if client_info else None,
        "last_name": client_info.last_name if client_info else None,
        "status": self.status,
        "last_updated": self.last_updated.strftime('%Y-%m-%d') if self.last_updated else None,
    }

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
