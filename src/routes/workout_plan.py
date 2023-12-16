from flask import make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.workoutplan_services import *

workoutplan_ns = Namespace(
    'workout plans', description='Workout plans related operations')

create_workoutplan_model = workoutplan_ns.model('Create Workout Plan', {
    'plan_name': fields.String(description='Workout Plan Name'),
    'plan_description': fields.String(description='Workout Plan Description'),
    'start_date': fields.Date(description='Workout Plan Start Date'),
    'end_date': fields.Date(description='Workout Plan End Date')
})

update_workoutplan_model = workoutplan_ns.model('Update Workout Plan', {
    'link_id': fields.Integer(description='Workout Plan Link ID'),
    'sequence': fields.Integer(description='Exercise sequence')
})

add_workout_to_plan_model = workoutplan_ns.model('AddWorkoutToPlan', {
    'workout_id': fields.Integer(required=True, description='ID of the workout to add'),
    'sequence': fields.Integer(required=True, description='Sequence of the workout in the plan'),
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


@workoutplan_ns.route('/planid<int:plan_id>')
class WorkoutPlan(Resource):

  @jwt_required()
  def get(self, plan_id):
    """Get all workouts from plan"""
    result, status_code = get_workouts_by_plan(plan_id)
    return make_response(result, status_code)

  @jwt_required()
  @workoutplan_ns.expect(add_workout_to_plan_model)
  def post(self, plan_id):
    """Add a workout to plan"""
    data = request.get_json()
    result, status_code = add_workout_to_plan(plan_id, data)
    return make_response(result, status_code)

  @jwt_required()
  def delete(self, plan_id):
    """Delete a plan"""
    result, status_code = delete_plan(plan_id)
    return make_response(result, status_code)


@workoutplan_ns.route('/linkid<int:link_id>')
class WorkoutsinPlan(Resource):

  @jwt_required()
  def delete(self, link_id):
    """Delete a workout from plan"""
    result, status_code = delete_workout_from_plan(link_id)
    return make_response(result, status_code)

  def update(self, link_id):
    """Update a workout in plan"""
    data = request.get_json()
    result, status_code = update_workout_in_plan(link_id, data)
    return make_response(result, status_code)

  def get(self, link_id):
    """Get a workout in plan"""
    result, status_code = get_workout_in_plan(link_id)
    return make_response(result, status_code)
