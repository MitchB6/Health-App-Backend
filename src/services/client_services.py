from flask_jwt_extended import get_jwt_identity

from ..models.survey_model import Survey
from ..models.coachmemberslink_model import CoachesMembersLink
from ..models.coach_model import CoachInfo
from ..models.workout_model import Workout

from ..extensions import db


def get_all_clients():
  coach = CoachInfo.query.filter_by(member_id=get_jwt_identity()).first()
  if not coach:
    return {'message': 'Not a coach or coach not found'}, 404

  clients = CoachesMembersLink.query.filter_by(
      coach_id=coach.coach_id, status="approved").all()

  if clients:
    serialized_clients = [client.serialize() for client in clients]
    return serialized_clients, 200
  else:
    return {"message": "No clients found"}, 404


def get_client_requests():
  try:
    coach = CoachInfo.query.filter_by(member_id=get_jwt_identity()).first()
    if not coach:
      return {'message': 'Not a coach or coach not found'}, 404

    requests = CoachesMembersLink.query.filter_by(
        coach_id=coach.coach_id, status="pending").all()

    serialized_requests = [request.serialize() for request in requests]
    return serialized_requests, 200
  except Exception as e:
    return {'message': 'An error occurred while fetching requests'}, 500


def accept_client_request(request_id):
  request = CoachesMembersLink.query.get(request_id)
  if request:
    request.status = 'approved'
    db.session.commit()
    return {'message': 'Client request accepted'}, 200
  return {'message': 'Request not found'}, 404


def decline_client_request(request_id):
  request = CoachesMembersLink.query.get(request_id)
  if request:
    db.session.delete(request)
    db.session.commit()
    return {'message': 'Client request declined'}, 200
  return {'message': 'Request not found'}, 404


def get_client_dashboard(client_id):
  query = CoachInfo.query.filter_by(member_id=get_jwt_identity())
  coach = query.first()
  if not coach:
    return {'message': 'Not a coach'}, 404
  link = CoachesMembersLink.query.filter_by(
      coach_id=coach.coach_id, member_id=client_id, status='approved').first()
  if link.status != 'approved':
    return {'message': 'Not a client'}, 404

  # Assuming there's a Workout model linked to a Member
  workouts = Workout.query.filter_by(member_id=client_id).all()
  # Assuming there's a Survey model linked to a Member
  surveys = Survey.query.filter_by(member_id=client_id).all()

  return {
      'workouts': [workout.serialize() for workout in workouts],
      'surveys': [survey.serialize() for survey in surveys]
  }
