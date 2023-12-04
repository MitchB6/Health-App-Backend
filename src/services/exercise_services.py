from flask import jsonify
from ..models.exercise_model import Exercise
from ..extensions import db

muscle_group = ['Abdominals', 'Adductors', 'Biceps', 'Calves', 'Chest', 'Forearms',
                'Glutes', 'Hamstrings', 'Lats', 'Lower Back', 'Middle Back', 'Traps',
                'Neck', 'Quadriceps', 'Shoulders', 'Triceps'
                ]

equipment = ['Bands', 'Barbell', 'Kettlebells', 'Dumbbell', 'Other', 'Cable', 'Machine',
             'Body Only', 'Medicine Ball', 'None', 'Exercise Ball', 'Foam Roll', 'E-Z Curl Bar']

sample_exercises = ['Crunch',
                    'Decline band press sit-up',
                    'FYR2 Banded Frog Pump',
                    'Band low-to-high twist',
                    'Barbell roll-out',
                    'Barbell Ab Rollout - On Knees',
                    'Decline bar press sit-up',
                    'Bench barbell roll-out'
                    ]


def get_equipment():
  return jsonify(equipment), 200


def get_muscle_group():
  return jsonify(muscle_group), 200


def get_sample_exercises():
  return jsonify(sample_exercises), 200


def marshal_exercise(exercise):
  return {
      'name': exercise.name,
      'description': exercise.description,
      'muscle_group': exercise.muscle_group,
      'equipment': exercise.equipment
  }


def get_all_exercises(muscle_group=None, equipment=None):
  """Get all exercises"""
  try:
    query = Exercise.query
    if muscle_group:
      query = query.filter(Exercise.muscle_group == muscle_group)
    if equipment:
      query = query.filter(Exercise.equipment == equipment)

    exercises = query.all()
    exercises_data = [marshal_exercise(exercise) for exercise in exercises]
    return exercises_data, 200
  except Exception as e:
    return {"message": str(e)}, 500


def create_exercise(data):
  """Create an exercise"""
  try:
    new_exercise = Exercise(
        name=str(data["name"]),
        description=str(data.get("description")),
        muscle_group=str(data.get("muscle_group")),
    )
    new_exercise.save()

    return {"message": f"Exercise created successfully: {new_exercise.exercise_id}"}, 201
  except Exception as e:
    return {"message": str(e)}, 400


def get_exercise_by_id(id):
  """Get an exercise by its id"""
  try:
    exercise = Exercise.query.get_or_404(id)
    exercise_data = marshal_exercise(exercise)
    return exercise_data, 200
  except Exception as e:
    return {"message": str(e)}, 404


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
    return {"message": str(e)}, 400


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
    return {"message": str(e)}, 400


def deactivate_exercise_by_id(id):
  try:
    exercise = Exercise.query.get_or_404(id)
    exercise.update(is_active=False)
    return {"message": "Exercise deactivated successfully"}, 200
  except Exception as e:
    return {"message": str(e)}, 400
