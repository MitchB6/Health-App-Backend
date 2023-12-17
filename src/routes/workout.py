from ..extensions import db
from flask import request, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.workout_services import *
from ..services.decorators import coach_required

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
    'sets': fields.Integer(description='Number of sets'),
    'reps': fields.Integer(description='Number of repetitions'),
    'sequence': fields.Integer(description='Exercise sequence'),
    'notes': fields.String(description='Additional notes'),
})

create_workout_stat = workout_ns.model('Create Workout Stat', {
    'duration': fields.Integer(description='Duration of the workout'),
    'calories_burned': fields.Integer(description='Calories burned')
})


@workout_ns.route('/')
class WorkoutList(Resource):
  @jwt_required()
  def get(self):
    """
    Get all workouts
    GOOD
    """
    result, status_code = get_member_workouts()
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(workout_model)
  def post(self):
    """
    Create a new workout
    GOOD
    """
    data = request.get_json()
    result, status_code = create_workout(data)
    return make_response(result, status_code)


@workout_ns.route('/<int:workout_id>/')
class Workout(Resource):
  @jwt_required()
  def get(self, workout_id):
    """
    Get a specific workout
    GOOD
    """
    result, status_code = get_workout(workout_id)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(workout_model)
  def put(self, workout_id):
    """
    Update an existing workout
    GOOD
    """
    data = request.get_json()
    result, status_code = update_workout(workout_id, data)
    return make_response(result, status_code)

  @jwt_required()
  def delete(self, workout_id):
    """
    Delete an existing workout
    GOOD
    """
    result, status_code = delete_workout(workout_id)
    return make_response(result, status_code)


@workout_ns.route('/<int:workout_id>/workout_exercises')
class WorkoutExercises(Resource):
  @jwt_required()
  def get(self, workout_id):
    """
    Get all exercises for a specific workout
    GOOD
    """
    result, status_code = get_workout_exercises(workout_id)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(create_workout_exercise_link)
  def post(self, workout_id):
    """
    Add an exercise to a workout
    GOOD
    """
    data = request.get_json()
    result, status_code = add_exercise_to_workout(workout_id, data)
    return make_response(result, status_code)


@workout_ns.route('/workout_exercise/<int:workout_exercise_id>')
class WorkoutExercisesID(Resource):
  @jwt_required()
  @workout_ns.expect(update_workout_exercise_link)
  def put(self, workout_exercise_id):
    """
    Update an exercise within a workout
    GOOD
    """
    data = request.get_json()
    result, status_code = update_exercise_in_workout(
        workout_exercise_id, data)
    return make_response(result, status_code)

  @jwt_required()
  def delete(self, workout_exercise_id):
    """
    Delete an exercise from a workout
    GOOD
    """
    result, status_code = delete_exercise_from_workout(
        workout_exercise_id)
    return make_response(result, status_code)


@workout_ns.route('/<int:workout_id>/stats')
class WorkoutStats(Resource):
  @jwt_required()
  def get(self, workout_id):
    """
    Get all stats for a specific workout
    GOOD
    """
    result, status_code = get_workout_stats(workout_id)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(create_workout_stat)
  def post(self, workout_id):
    """
    Add a stat to a workout
    GOOD
    """
    data = request.get_json()
    result, status_code = add_stat_to_workout(workout_id, data)
    return make_response(result, status_code)


@workout_ns.route('/workout_stat/<int:workout_stat_id>')
class WorkoutStatsID(Resource):
  @jwt_required()
  def get(self, workout_stat_id):
    """
    Get a workout's specific stat
    GOOD
    """
    result, status_code = get_workout_stat(workout_stat_id)
    return make_response(result, status_code)

  def delete(self, workout_stat_id):
    """
    Delete a workout's specific stat
    """
    result, status_code = delete_workout_stat(workout_stat_id)
    return make_response(result, status_code)


@workout_ns.route('/member/<int:member_id>')
class WorkoutsMemberID(Resource):
  @jwt_required()
  def get(self, member_id):
    """
    Get all workouts for a specific member
    GOOD
    """
    result, status_code = get_workouts_by_member(member_id)

    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(workout_model)
  def post(self, member_id):
    """
    Create a new workout for a specific member
    GOOD
    """
    data = request.get_json()
    result, status_code = create_workout_for_member(member_id, data)
    return make_response(result, status_code)


@workout_ns.route('/member/<int:member_id>/workout/<int:workout_id>')
class WorkoutsMemberIDWorkoutID(Resource):
  @jwt_required()
  def get(self, member_id, workout_id):
    """
    Get a specific workout for a specific member
    GOOD
    """
    result, status_code = get_workout_for_member(member_id, workout_id)
    return make_response(result, status_code)

  @jwt_required()
  @workout_ns.expect(workout_model)
  def put(self, member_id, workout_id):
    """
    Update an existing workout for a specific member
    GOOD
    """
    data = request.get_json()
    result, status_code = update_workout_for_member(
        data, member_id, workout_id)
    return make_response(result, status_code)

  @jwt_required()
  def delete(self, member_id, workout_id):
    """
    Delete an existing workout for a specific member
    GOOD
    """
    result, status_code = delete_workout_for_member(member_id, workout_id)
    return make_response(result, status_code)
