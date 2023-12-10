from flask import make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.workoutplan_services import *

workoutplan_ns = Namespace(
    'workout plans', description='Workout plans related operations')

create_workoutplan_model = workoutplan_ns.model('Create Workout Plan', {
    'plan_id': fields.Integer(description='Workout Plan ID'),
    'workout_id': fields.Integer(description='Workout ID'),
    'sequence': fields.Integer(description='Exercise sequence')
})

update_workoutplan_model = workoutplan_ns.model('Update Workout Plan', {
    'link_id': fields.Integer(description='Workout Plan Link ID'),
    'sequence': fields.Integer(description='Exercise sequence')
})


@workoutplan_ns.route('/')
class PlansList(Resource):
  @jwt_required()
  def get(self):
    """Get all plans"""
    result, status_code = get_member_plans()
    return make_response(result, status_code)

  @jwt_required()
  @workoutplan_ns.expect(create_workoutplan_model)
  def post(self):
    """Create a new plan"""
    data = request.get_json()
    result, status_code = create_plan(data)
    return make_response(result, status_code)


@workoutplan_ns.route('/<int:plan_id>')
class WorkoutPlan(Resource):

  @jwt_required()
  def get(self, plan_id):
    """Get all workouts from plan"""
    result, status_code = get_workouts_by_plan(plan_id)
    return make_response(result, status_code)

  @jwt_required()
  @workoutplan_ns.expect(create_workoutplan_model)
  def post(self, plan_id):
    """Add a workout to plan"""
    data = request.get_json()
    result, status_code = add_workout_to_plan(plan_id, data)
    return make_response(result, status_code)

  @jwt_required()
  def delete(self, plan_id):
    """Delete a workout from plan"""
    link_id = request.args.get('link_id')
    result, status_code = delete_workout_from_plan(plan_id, link_id)
    return make_response(result, status_code)

  @jwt_required()
  @workoutplan_ns.expect(update_workoutplan_model)
  def put(self, plan_id):
    """Update a workout in plan"""
    link_id = request.args.get('link_id')
    result, status_code = update_workout_in_plan(plan_id, link_id)
    return make_response(result, status_code)
