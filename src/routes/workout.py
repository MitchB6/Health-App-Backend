from ..extensions import db
from flask import request, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.workout_services import *
from ..models.workoutplanlink_model import WorkoutPlanLink

workout_ns = Namespace('workouts', description='Workout related operations')


workout_model = workout_ns.model('Workout', {
    'workout_name': fields.String(required=True, description='Name of the workout')
})

workout_exercise_link = workout_ns.model('Workout_Exercise', {
    'workout_exercise_id': fields.Integer(description='Workout Exercise ID'),
    'workout_id': fields.Integer(required=True, description='Workout ID'),
    'exercise_id': fields.Integer(required=True, description='Exercise ID'),
    'sets': fields.Integer(description='Number of sets'),
    'reps': fields.Integer(description='Number of repetitions'),
    'sequence': fields.Integer(description='Exercise sequence'),
    'notes': fields.String(description='Additional notes'),
})

create_workout_exercise_link = workout_ns.model('Create Workout_Exercise', {
    'exercise_id': fields.Integer(description='Exercise ID'),
    'sets': fields.Integer(description='Number of sets'),
    'reps': fields.Integer(description='Number of repetitions'),
    'sequence': fields.Integer(description='Exercise sequence'),
    'notes': fields.String(description='Additional notes'),
})

update_workout_exercise_link = workout_ns.model('Update Workout_Exercise', {
    'workout_exercise_id': fields.Integer(description='Workout Exercise ID'),
    'sets': fields.Integer(description='Number of sets'),
    'reps': fields.Integer(description='Number of repetitions'),
    'sequence': fields.Integer(description='Exercise sequence'),
    'notes': fields.String(description='Additional notes'),
})


@workout_ns.route('/')
class WorkoutList(Resource):
  @jwt_required()
  def get(self):
    """Get all workouts"""
    result, status_code = get_member_workouts()
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(workout_model)
  def post(self):
    """Create a new workout"""
    data = request.get_json()
    result, status_code = create_workout(data)
    return make_response(result, status_code)


@workout_ns.route('/<int:workout_id>')
class Workout(Resource):
  @jwt_required()
  @workout_ns.expect(workout_model)
  def put(self, workout_id):
    """Update an existing workout"""
    data = request.get_json()
    result, status_code = update_workout(workout_id, data)
    return make_response(result, status_code)

  @jwt_required()
  def delete(self, workout_id):
    """Delete an existing workout"""
    result, status_code = delete_workout(workout_id)
    return make_response(result, status_code)


@workout_ns.route('/member/<int:member_id>')
class WorkoutsForMember(Resource):
  @jwt_required()
  def get(self, member_id):
    """Get all workouts for a specific member"""
    result, status_code = get_workouts_by_member(member_id)
    return make_response(result, status_code)


@workout_ns.route('/<int:workout_id>/exercises')
class WorkoutExercises(Resource):
  @jwt_required()
  @workout_ns.doc(params={'workout_id': 'ID of the workout'})
  def get(self, workout_id):
    """Get all exercises for a specific workout"""
    result, status_code = get_workout_exercises(workout_id)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(create_workout_exercise_link)
  def post(self, workout_id):
    """Add an exercise to a workout"""
    data = request.get_json()
    result, status_code = add_exercise_to_workout(workout_id, data)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(update_workout_exercise_link)
  def put(self, workout_id):
    """Update an exercise within a workout"""
    data = request.get_json()
    result, status_code = update_exercise_in_workout(workout_id, data)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.doc(params={'workout_exercise_id': 'Workout Exercise ID'})
  def delete(self, workout_id):
    """Delete an exercise from a workout"""
    workout_exercise_id = request.args.get('workout_exercise_id')
    result, status_code = delete_exercise_from_workout(workout_exercise_id)
    return make_response(result, status_code)
