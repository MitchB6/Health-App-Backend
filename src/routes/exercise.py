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
    }
)

exercise_list_args = exercise_ns.model(
    'ExerciseListArgs', {
        'name': fields.String(description='Filter by name'),
        'muscle_group': fields.String(description='Filter by muscle group'),
        'equipment': fields.String(description='Filter by equipment')
    }
)


@exercise_ns.route('/')
class ExerciseList(Resource):
  @exercise_ns.expect(exercise_list_args, validate=True, optional=True)
  def get(self):
    """List all exercises"""
    name = request.args.get('name', None)
    muscle_group = request.args.get('muscle_group', None)
    equipment = request.args.get('equipment', None)
    result, status_code = search_exercises(name, muscle_group, equipment)
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
  @jwt_required()
  @admin_required
  def delete(self, id):
    """Delete an exercise"""
    result, status_code = delete_exercise(id)
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/update')
class ExerciseUpdate(Resource):
  @jwt_required()
  @admin_required
  @exercise_ns.expect(exercise_model)
  def put(self, id):
    """Update an exercise"""
    data = request.get_json()
    result, status_code = update_exercise(id, data)
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/activate/all')
class ActivateAllExercises(Resource):
  @jwt_required()
  @admin_required
  def put(self):
    result, status_code = activate_all_exercises()
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/deactivate/all')
class DeactivateAllExercises(Resource):
  @jwt_required()
  @admin_required
  def put(self):
    result, status_code = deactivate_all_exercises()
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/activate/<int:id>')
class ActivateExerciseById(Resource):
  @jwt_required()
  @admin_required
  def put(self, id):
    result, status_code = activate_exercise_by_id(id)
    return make_response(jsonify(result), status_code)


@exercise_ns.route('/deactivate/<int:id>')
class DeactivateExerciseById(Resource):
  @jwt_required()
  @admin_required
  def put(self, id):
    result, status_code = deactivate_exercise_by_id(id)
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
