from flask_jwt_extended import get_jwt_identity

from ..models.workout_model import Workout
from ..models.workoutexercise_model import WorkoutExercise
from ..models.workoutstat_model import WorkoutStat
from ..models.coachmemberslink_model import CoachesMembersLink


def verify_coach_member_link(member_id):
  coach_id = get_jwt_identity()
  link = CoachesMembersLink.query.filter_by(
      coach_id=coach_id, member_id=member_id, status='approved').first()
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
  new_workout.save()
  response, status_code = {"message": "Workout created successfully"}, 201
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
  link = verify_coach_member_link(member_id)

  if link:
    new_workout = Workout(
        workout_name=data.get('workout_name'),
        member_id=member_id
    )
    new_workout.save()
    response, status_code = {"message": "Workout created successfully"}, 201
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def update_workout_for_member(member_id, data):
  link = verify_coach_member_link(member_id)

  if link:
    workout = Workout.query.get_or_404(data.get('workout_id'))
    workout.workout_name = data.get('workout_name', workout.workout_name)
    workout.save()
    response, status_code = {"message": "Workout updated successfully"}, 200
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def delete_workout_for_member(member_id, workout_id):
  link = verify_coach_member_link(member_id)

  if link:
    workout = Workout.query.get_or_404(workout_id)
    workout.delete()
    response, status_code = {"message": "Workout deleted successfully"}, 200
  else:
    response, status_code = {'message': 'Access denied'}, 404

  return response, status_code


def get_workout_exercises(workout_id):
  # Find all exercises for a specific workout
  exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).all()

  # Serialize the exercises
  serialized_exercises = [exercise.serialize() for exercise in exercises]

  return serialized_exercises, 200


def add_exercise_to_workout(workout_id, data):

  new_workout_exercise = WorkoutExercise(
      workout_id=workout_id,
      exercise_id=data.get('exercise_id'),
      sets=data.get('sets'),
      reps=data.get('reps'),
      sequence=data.get('sequence'),
      notes=data.get('notes')
  )
  new_workout_exercise.save()
  return {"message": "Exercise added to workout successfully"}, 201


def update_exercise_in_workout(workout_exercise_id, data):
  """Update an exercise within a workout"""

  exercise = WorkoutExercise.query.filter_by(
      workout_exercise_id=workout_exercise_id).first()
  if exercise:
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


def delete_stat_from_workout(stat_id):
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
