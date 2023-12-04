from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from flask import request, jsonify, make_response

from ..services.exercise_services import *
from ..services.decorators import admin_required

exercise_ns = Namespace('exercise', description='A namespace for Exercise')

exercise_model = exercise_ns.model(
    'Exercise', {
        'name': fields.String(required=True),
        'description': fields.String(),
        'muscle_group': fields.String(),
        'equipment': fields.String()
    })


@exercise_ns.route('/')
class ExerciseList(Resource):
  def get(self):
    """List all exercises"""
    muscle_group = request.args.get('muscle_group', None)
    equipment = request.args.get('equipment', None)
    result, status_code = get_all_exercises(muscle_group, equipment)
    return make_response(jsonify(result), status_code)

  @jwt_required()
  @admin_required
  @exercise_ns.expect(exercise_model)
  def post(self):
    """Create a new exercaise"""
    data = request.get_json()
    result, status_code = create_exercise(data)
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/<int:id>')
class Exercise(Resource):
  def get(self):
    """Fetch a single exercise"""
    data = request.get_json()
    result, status_code = get_exercise_by_id(data)
    return make_response(jsonify(result), status_code)

  @jwt_required()
  @admin_required
  @exercise_ns.expect(exercise_model)
  def put(self, id):
    """Update an exercise"""
    data = request.get_json()
    result, status_code = update_exercise(id, data)
    return make_response(jsonify(result), status_code)

  @jwt_required()
  @admin_required
  def delete(self, id):
    """Delete an exercise"""
    result, status_code = delete_exercise(id)
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/equipment')
class GetEquipment(Resource):
  @staticmethod
  def get():
    """Fetch all equipment"""
    result, status_code = get_equipment()
    return make_response(result, status_code)


@exercise_ns.route('/muscle_group')
class GetMuscleGroup(Resource):
  @staticmethod
  def get():
    """Fetch all muscle groups"""
    result, status_code = get_muscle_group()
    return make_response(result, status_code)


@exercise_ns.route('/sample_exercises')
class GetSampleExercises(Resource):
  @staticmethod
  def get():
    """Fetch sample exercises"""
    result, status_code = get_sample_exercises()
    return make_response(result, status_code)
