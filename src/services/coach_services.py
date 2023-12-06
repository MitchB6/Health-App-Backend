from ..models.coach_model import CoachInfo
from ..models.coachmemberslink_model import CoachesMembersLink
from ..extensions import db


def get_all_coaches():
  coaches = CoachInfo.all_coaches()
  serialized_coaches = [coach.serialize() for coach in coaches]
  return serialized_coaches, 200


def get_coach(coach_id):
  coach = CoachInfo.query.get(coach_id)
  if coach:
    serialized_coach = coach.serialize()
    return serialized_coach, 200
  else:
    return {"message": "Coach not found"}, 404


def link_request(data):
  client_name = data['client_name']
  coach_id = data['coach_id']

  if not client_name or not coach_id:
    return {'message': 'Client name and coach ID are required'}, 400

  coach = CoachInfo.query.get(coach_id)

  if not coach:
    return {'message': 'Coach not found'}, 404

  link_request = CoachesMembersLink(client_name=client_name, coach=coach)
  db.session.add(link_request)
  db.session.commit()

  return {'message': 'Hire request submitted successfully'}, 201
