from ..models.coach_model import CoachInfo
from ..models.coachmemberslink_model import CoachesMembersLink
from ..extensions import db


def search_coaches(specialization=None, price=0.00, location=None):
  query = CoachInfo.query.filter_by(approved=True)

  if specialization:
    query = query.filter_by(specialization=specialization)

  if price is not None:
    price = float(price)
    if price > 0.00:
      query = query.filter(CoachInfo.price <= price)

  if location:
    query = query.filter_by(location=location)

  coaches = query.all()

  if coaches:
    serialized_coaches = [coach.serialize() for coach in coaches]
    return serialized_coaches, 200
  else:
    return {"message": "No coaches found"}, 404


def link_request(data):
  member_id = data.get('member_id')
  coach_id = data.get('coach_id')

  if not member_id or not coach_id:
    return {'message': 'Client name and coach ID are required'}, 400

  coach = CoachInfo.query.get(coach_id)

  if not coach:
    return {'message': 'Coach not found'}, 404

  existing_link = CoachesMembersLink.query.filter_by(
      coach_id=coach_id, member_id=member_id).first()

  if not existing_link:
    new_link = CoachesMembersLink(coach_id=coach.coach_id, member_id=member_id)
    db.session.add(new_link)
    db.session.commit()

  return {'message': 'Hire request submitted successfully'}, 201
