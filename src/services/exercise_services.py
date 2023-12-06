from flask import jsonify
import random

from ..models.exercise_model import Exercise
from ..extensions import db


def marshal_exercise(exercise):
  return {
      'name': exercise.name,
      'description': exercise.description,
      'muscle_group': exercise.muscle_group,
      'equipment': exercise.equipment
  }


def get_equipment():
  try:
    equipment = db.session.query(Exercise.equipment).distinct().all()
    equipment = [result[0] for result in equipment]
    return jsonify(equipment), 200
  except Exception as e:
    return {"message": str(e)}, 500


def get_muscle_group():
  try:
    muscle_groups = db.session.query(Exercise.muscle_group).distinct().all()
    muscle_groups = [result[0] for result in muscle_groups]
    return jsonify(muscle_groups), 200
  except Exception as e:
    return {"message": str(e)}, 500


def get_sample_exercises():
  try:
    # Get a list of all exercise names
    all_exercise_names = Exercise.query.with_entities(Exercise.name).all()
    all_exercise_names = [name[0] for name in all_exercise_names]

    # Randomly select 10 unique exercise names
    sample_exercise_names = random.sample(all_exercise_names, 10)

    return jsonify(sample_exercise_names), 200
  except Exception as e:
    return {"message": str(e)}, 500


def search_exercises(name=None, muscle_group=None, equipment=None):
  """Get all exercises"""
  query = Exercise.query
  if name:
    query = query.filter(Exercise.name.ilike(f"%{name}%"))
  if muscle_group:
    query = query.filter(Exercise.muscle_group == muscle_group)
  if equipment:
    query = query.filter(Exercise.equipment == equipment)

  exercises = query.all()
  exercises_data = [marshal_exercise(exercise) for exercise in exercises]
  return exercises_data, 200


def create_exercise(data):
  """Create an exercise"""
  new_exercise = Exercise(
      name=str(data["name"]),
      description=str(data.get("description")),
      muscle_group=str(data.get("muscle_group")),
  )
  new_exercise.save()

  return {"message": f"Exercise created successfully: {new_exercise.exercise_id}"}, 201


def update_exercise(exercise_id, data):
  """Update an exercise"""
  try:
    exercise = Exercise.query.get_or_404(exercise_id)
    exercise.update(**data)
    return {"message": "Exercise updated successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 400


def delete_exercise(exercise_id):
  """Delete an exercise"""
  try:
    exercise = Exercise.query.get_or_404(exercise_id)
    exercise.delete()
    return {"message": "Exercise deleted successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 500


def activate_all_exercises():
  try:
    # Activate all exercises
    Exercise.query.update({"is_active": True})
    db.session.commit()
    return {"message": "All exercises activated successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 500


def deactivate_all_exercises():
  try:
    # Deactivate all exercises
    Exercise.query.update({"is_active": False})
    db.session.commit()
    return {"message": "All exercises deactivated successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 500


def activate_exercise_by_id(id):
  try:
    exercise = Exercise.query.get_or_404(id)
    exercise.update(is_active=True)
    return {"message": "Exercise activated successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 500


def deactivate_exercise_by_id(id):
  try:
    exercise = Exercise.query.get_or_404(id)
    exercise.update(is_active=False)
    return {"message": "Exercise deactivated successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 500
