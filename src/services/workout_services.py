from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from ..models.workout_model import Workout


def create_workout(data):
  current_member_id = get_jwt_identity()
  workout_name = data.get('workout_name')
  energy_level = data.get('energy_level')

  # Validate workout

  workout = Workout(
      member_id=current_member_id,
      workout_name=workout_name,
      energy_level=energy_level
  )

  workout.save()

  return {"message": "Workout created successfully"}, 201


def update_workout(workout_id, data):
  # Find the workout by ID
  workout = Workout.query.get_or_404(workout_id)

  # Validate workout update

  # Update workout attributes
  workout.workout_name = data.get('workout_name', workout.workout_name)
  workout.workout_date = data.get('workout_date', workout.workout_date)
  workout.energy_level = data.get('energy_level', workout.energy_level)

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
