from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from ..models.workoutplan_model import WorkoutPlan
from ..models.workoutplanlink_model import WorkoutPlanLink


def create_plan(data):
  """Create a new plan"""
  member_id = get_jwt_identity()
  new_plan = WorkoutPlan(
      member_id=member_id,
      plan_name=data.get('plan_name'),
      description=data.get('plan_description')
  )
  new_plan.create()
  return {"message": "Plan created successfully"}, 201


def get_member_plans():
  member_id = get_jwt_identity()
  """Get all workout plans for a member"""
  try:
    plans = WorkoutPlan.query.filter_by(member_id=member_id).all()
    plans_data = [plan.serialize() for plan in plans]
    return jsonify(plans_data), 200
  except Exception as e:
    return {"message": str(e)}, 500


def delete_plan(plan_id):
  """Delete a plan"""
  plan = WorkoutPlan.query.filter_by(plan_id=plan_id).first()
  if plan:
    plan.delete()
    return {"message": "Plan deleted successfully"}, 200
  else:
    return {"message": "Plan not found"}, 404


def get_workouts_by_plan(plan_id):
  """Get all workouts from plan"""
  workouts = WorkoutPlanLink.query.filter_by(plan_id=plan_id).all()

  # Serialize the exercises
  serialized_workouts = [workout.serialize_workout_in_plan()
                         for workout in workouts]

  return serialized_workouts, 200


def add_workout_to_plan(plan_id, data):
  new_workout_plan_link = WorkoutPlanLink(
      plan_id=plan_id,
      workout_id=data.get('workout_id'),
      sequence=data.get('sequence')
  )
  new_workout_plan_link.save()
  return {"message": "Workout added to plan successfully"}, 201


def delete_workout_from_plan(link_id):
  workout_plan_link = WorkoutPlanLink.query.filter_by(
      link_id=link_id).first()
  if workout_plan_link:
    workout_plan_link.delete()
    return {"message": "Workout deleted from plan successfully"}, 200
  else:
    return {"message": "Workout not found in plan"}, 404


def update_workout_in_plan(data):
  link_id = data.get("link_id")
  workout_plan_link = WorkoutPlanLink.query.filter_by(
      link_id=link_id).first()
  if workout_plan_link:
    workout_plan_link.sequence = data.get('sequence')
    workout_plan_link.save()
    return {"message": "Workout updated in plan successfully"}, 200
  else:
    return {"message": "Workout not found in plan"}, 404


def get_workout_in_plan(link_id):
  workout_plan_link = WorkoutPlanLink.query.filter_by(
      link_id=link_id).first()
  if workout_plan_link:
    return workout_plan_link.serialize_workout_in_plan(), 200
  else:
    return {"message": "Workout not found in plan"}, 404
