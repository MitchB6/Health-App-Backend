from flask_jwt_extended import get_jwt_identity

from ..models.workout_model import Workout
from ..models.workoutexercise_model import WorkoutExercise
from ..models.workoutstat_model import WorkoutStat
from ..models.coachmemberslink_model import CoachesMembersLink
from ..models.coach_model import CoachInfo
from ..extensions import db


def verify_coach_member_link(member_id):
  query = CoachInfo.query.filter_by(member_id=get_jwt_identity())
  coach = query.first()
  if not coach:
    return 404
  else:
    link = CoachesMembersLink.query.filter_by(
        coach_id=coach.coach_id, member_id=member_id, status='approved').first()

  return link


def get_member_workouts():
  member_id = get_jwt_identity()

  # Find all workouts for a specific member
  workouts = Workout.query.filter_by(member_id=member_id)

  # Serialize the workouts
  response, status_code = [workout.serialize() for workout in workouts], 200

  return response, status_code


def create_workout(data):
  new_workout = Workout(
      workout_name=str(data.get('workout_name')),
      member_id=get_jwt_identity()
  )
  db.session.add(new_workout)
  db.session.flush()
  db.session.commit()

  response, status_code = {
      "message": f"Workout created successfully : {new_workout.workout_id}"}, 201
  return response, status_code


def get_workout(workout_id):
  workout = Workout.query.filter_by(workout_id=workout_id).first()
  if workout:
    response, status_code = workout.serialize(), 200
  else:
    response, status_code = {"message": "Workout not found"}, 404
  return response, status_code


def update_workout(workout_id, data):
  # Find the workout by ID
  workout = Workout.query.get_or_404(workout_id)

  workout.workout_name = data.get('workout_name', workout.workout_name)

  # Save the updated workout to the database
  workout.save()
  response, status_code = {"message": "Workout updated successfully"}, 200
  return response, status_code


def delete_workout(workout_id):
  # Find the workout by ID
  workout = Workout.query.get_or_404(workout_id)

  # Delete the workout from the database
  workout.delete()
  response, status_code = {"message": "Workout deleted successfully"}, 200
  return response, status_code


def get_workouts_by_member(member_id):
  link = verify_coach_member_link(member_id)

  if link:
    """Get all workouts for a specific member"""
    workouts = Workout.query.filter_by(member_id=member_id)
    response, status_code = [
        workout.serialize() for workout in workouts], 200
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def create_workout_for_member(member_id, data):
  """Create a new workout for a specific member"""
  link = verify_coach_member_link(member_id)

  if link != 404:
    new_workout = Workout(
        workout_name=data.get('workout_name'),
        member_id=member_id
    )
    new_workout.save()
    response, status_code = {
        "message": f"Workout created successfully {new_workout.workout_id}"}, 201
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def get_workout_for_member(member_id, workout_id):
  """Get a specific workout for a specific member"""
  link = verify_coach_member_link(member_id)

  if link != 404:
    workout = Workout.query.filter_by(
        member_id=member_id, workout_id=workout_id).first()
    if workout:
      response, status_code = workout.serialize(), 200
    else:
      response, status_code = {"message": "Workout not found"}, 404
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def update_workout_for_member(data, member_id, workout_id):
  """Update an existing workout for a specific member"""
  link = verify_coach_member_link(member_id)

  if link != 404:
    workout = Workout.query.filter_by(
        member_id=member_id, workout_id=workout_id).first()
    workout.workout_name = data.get('workout_name', workout.workout_name)
    workout.save()
    response, status_code = {"message": "Workout updated successfully"}, 200
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def delete_workout_for_member(member_id, workout_id):
  """Delete an existing workout from a member"""
  link = verify_coach_member_link(member_id)

  if link != 404:
    workout = Workout.query.get_or_404(workout_id)
    workout.delete()
    response, status_code = {"message": "Workout deleted successfully"}, 200
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def get_workout_exercises(workout_id):
  """Get all exercises for a specific workout"""
  exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).all()

  serialized_exercises = [exercise.serialize() for exercise in exercises]

  return serialized_exercises, 200


def add_exercise_to_workout(workout_id, data):
  """Add an exercise to a workout"""
  new_workout_exercise = WorkoutExercise(
      workout_id=workout_id,
      exercise_id=data.get('exercise_id'),
      sets=data.get('sets'),
      reps=data.get('reps'),
      sequence=data.get('sequence'),
      notes=data.get('notes')
  )
  new_workout_exercise.save()
  return {"message": f"Exercise added to workout successfully: {new_workout_exercise.workout_exercise_id}"}, 201


def update_exercise_in_workout(workout_exercise_id, data):
  """Update an exercise within a workout"""

  exercise = WorkoutExercise.query.filter_by(
      workout_exercise_id=workout_exercise_id).first()
  if exercise:
    exercise.exercise_id = data.get('exercise_id')
    exercise.sets = data.get('sets')
    exercise.reps = data.get('reps')
    exercise.sequence = data.get('sequence')
    exercise.notes = data.get('notes')
    exercise.save()
    return {"message": "Exercise updated successfully"}, 200
  else:
    return {"message": "Exercise not found in workout"}, 404


def delete_exercise_from_workout(workout_exercise_id):
  """Delete an exercise from a workout"""
  exercise = WorkoutExercise.query.filter_by(
      workout_exercise_id=workout_exercise_id).first()
  if exercise:
    exercise.delete()
    return {"message": "Exercise deleted from workout successfully"}, 200
  else:
    return {"message": "Exercise not found in workout"}, 404


def get_workout_stats(workout_id):
  # Find all stats for a specific workout
  stats = WorkoutStat.query.filter_by(workout_id=workout_id).all()

  # Serialize the stats
  serialized_stats = [stat.serialize() for stat in stats]

  return serialized_stats, 200


def add_stat_to_workout(workout_id, data):
  new_workout_stat = WorkoutStat(
      workout_id=workout_id,
      duration=data.get('duration'),
      calories_burned=data.get('calories_burned'),
      date=data.get('date')
  )
  new_workout_stat.save()
  return {"message": "Stat added to workout successfully"}, 201


def delete_workout_stat(stat_id):
  stat = WorkoutStat.query.filter_by(stat_id=stat_id).first()
  if stat:
    stat.delete()
    return {"message": "Stat deleted from workout successfully"}, 200
  else:
    return {"message": "Stat not found in workout"}, 404


def update_stat_in_workout(stat_id, data):
  stat_id = data.get('stat_id')
  stat = WorkoutStat.query.filter_by(stat_id=stat_id).first()
  if stat:
    stat.duration = data.get('duration')
    stat.calories_burned = data.get('calories_burned')
    stat.date = data.get('date')
    stat.save()
    return {"message": "Stat updated successfully"}, 200
  else:
    return {"message": "Stat not found in workout"}, 404


def get_workout_stat(workout_stat_id):
  stat = WorkoutStat.query.filter_by(stat_id=workout_stat_id).first()
  if stat:
    return stat.serialize(), 200
  else:
    return {"message": "Stat not found in workout"}, 404
