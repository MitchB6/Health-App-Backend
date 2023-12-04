from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.workout_services import *

workout_ns = Namespace('workouts', description='Workout related operations')


workout_model = workout_ns.model('Workout', {
    'workout_name': fields.String(required=True, description='Name of the workout'),
    'workout_date': fields.Date(required=True, description='Date of the workout'),
    'energy_level': fields.Integer(description='Energy level during the workout'),
})


@workout_ns.route('/')
class WorkoutList(Resource):
  @jwt_required()
  def post(self):
    """Create a new workout"""
    data = request.get_json()
    result, status_code = create_workout(data)
    return result, status_code

  @jwt_required()
  def get(self):
    """Get all workouts"""
    result, status_code = get_workouts_by_member()
    return result, status_code


@workout_ns.route('/<int:workout_id>')
class Workout(Resource):
  @jwt_required()
  def put(self, workout_id):
    """Update an existing workout"""
    data = request.get_json()
    result, status_code = update_workout(workout_id, data)
    return result, status_code

  @jwt_required()
  def delete(self, workout_id):
    """Delete an existing workout"""
    result, status_code = delete_workout(workout_id)
    return result, status_code


@workout_ns.route('/<int:workout_id>')
class Workout(Resource):
  @jwt_required()
  def put(self, workout_id):
    """Update an existing workout"""
    data = request.get_json()
    result, status_code = update_workout(workout_id, data)
    return result, status_code

  @jwt_required()
  def delete(self, workout_id):
    """Delete an existing workout"""
    result, status_code = delete_workout(workout_id)
    return result, status_code


@workout_ns.route('/member/<int:member_id>')
class WorkoutsForMember(Resource):
  @jwt_required()
  def get(self, member_id):
    """Get all workouts for a specific member"""
    result, status_code = get_workouts_by_member(member_id)
    return result, status_code
