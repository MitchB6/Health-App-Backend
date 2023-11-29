from ..extensions import db
from .coachinfo_model import CoachInfo
from .member_model import Member

# The `CoachesMembersLink` class is a model that represents the link between coaches and members in a
# database, providing methods to create, remove, and find links between them.
class CoachesMembersLink(db.Model):
  __tablename__ = 'coaches_members_link'

  link_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), nullable=False)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  
  @classmethod
  def create_link(cls, coach_id, member_id):
    """Add new link if DNE"""
    existing_link = cls.query.filter_by(coach_id=coach_id, member_id=member_id).first()
    if not existing_link:
      new_link = cls(coach_id=coach_id, member_id=member_id)
      db.session.add(new_link)
      db.session.commit()
      return new_link
    return existing_link  # or handle this case as needed
  
  @classmethod
  def remove_link(cls, coach_id, member_id):
    """Remove link if exists"""
    link_to_remove = cls.query.filter_by(coach_id=coach_id, member_id=member_id).first()
    if link_to_remove:
      db.session.delete(link_to_remove)
      db.session.commit()

  @classmethod
  def find_coaches_by_member(cls, member_id):
    """Find coaches for specific member"""
    links = cls.query.filter_by(member_id=member_id).all()
    coach_ids = [link.coach_id for link in links]
    return CoachInfo.query.filter(CoachInfo.coach_id.in_(coach_ids)).all()

  @classmethod
  def find_members_by_coach(cls, coach_id):
    """Find members for specific coach"""
    links = cls.query.filter_by(coach_id=coach_id).all()
    member_ids = [link.member_id for link in links]
    return Member.query.filter(Member.member_id.in_(member_ids)).all()