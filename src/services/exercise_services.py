from ..models.exercise_model import Exercise


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
