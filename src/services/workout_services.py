from flask_jwt_extended import get_jwt_identity

from ..models.workout_model import Workout
from ..models.workoutexercise_model import WorkoutExercise


def get_member_workouts():
  member_id = get_jwt_identity()

  # Find all workouts for a specific member
  workouts = Workout.find_by_member(member_id)

  # Serialize the workouts
  serialized_workouts = [workout.serialize() for workout in workouts]

  return serialized_workouts, 200


def create_workout(data):
  new_workout = Workout(
      workout_name=str(data.get('workout_name')),
      member_id=get_jwt_identity()
  )
  new_workout.save()
  return {"message": "Workout created successfully"}, 201


def update_workout(workout_id, data):
  # Find the workout by ID
  workout = Workout.query.get_or_404(workout_id)

  workout.workout_name = data.get('workout_name', workout.workout_name)

  # Save the updated workout to the database
  workout.save()

  return {"message": "Workout updated successfully"}, 200


def delete_workout(workout_id):
  # Find the workout by ID
  workout = Workout.query.get_or_404(workout_id)

  # Delete the workout from the database
  workout.delete()

  return {"message": "Workout deleted successfully"}, 200


def get_workouts_by_member(member_id):
  # Find all workouts for a specific member
  workouts = Workout.find_by_member(member_id)

  # Validate member

  # Serialize the workouts
  serialized_workouts = [workout.serialize() for workout in workouts]

  return serialized_workouts, 200


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
  workout_exercise_id = data.get('workout_exercise_id')
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


def delete_exercise_from_workout(workout_id, workout_exercise_id):
  exercise = WorkoutExercise.query.filter_by(
      workout_exercise_id=workout_exercise_id).first()
  if exercise:
    exercise.delete()
    return {"message": "Exercise deleted from workout successfully"}, 200
  else:
    return {"message": "Exercise not found in workout"}, 404
