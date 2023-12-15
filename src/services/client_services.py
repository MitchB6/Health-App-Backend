from ..models.coach_model import CoachInfo
from ..models.survey_model import Survey
from ..models.coachmemberslink_model import CoachesMembersLink
from ..extensions import db
from ..models.workout_model import Workout
from ..models.workoutexercise_model import WorkoutExercise
from flask_jwt_extended import get_jwt_identity


def get_all_clients():
    query = CoachesMembersLink.query.filter_by(status="approved")
    clients = query.all()

    if clients:
        serialized_clients = [clients.serialized_members() for cleints in clients]
    else:
        return serialized_clients, 404
    
    return serialized_clients, 200

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
    workouts = Workout.query.filter_by(member_id=client_id).all()
    # Assuming there's a Survey model linked to a Member
    surveys = Survey.query.filter_by(member_id=client_id).all()

    return {
        'workouts': [workout.serialize() for workout in workouts],
        'surveys': [survey.serialize() for survey in surveys]
    }

def create_workout_plan(member_id, workout_details):
    new_workout = Workout(member_id=member_id, **workout_details)
    db.session.add(new_workout)
    db.session.commit()
    return new_workout.serialize(), 201


