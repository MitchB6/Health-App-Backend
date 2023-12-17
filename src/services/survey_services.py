from flask_jwt_extended import get_jwt_identity

from ..models.survey_model import Survey
from ..services.validations import *


def get_user_survey():
  member_id = get_jwt_identity()

  surveys = Survey.query.filter_by(member_id=member_id)
  if surveys:
    response, status_code = [survey.serialize() for survey in surveys], 200
  else:
    response, status_code = {"message": "No surveys found"}, 404

  return response, status_code


def create_user_survey(data):

  member_id = get_jwt_identity()
  mood_level = data.get('mood_level')
  hydration_level = data.get('hydration_level')
  calories_intake = data.get('calories_intake')
  if not mood_level or not hydration_level or not calories_intake:
    response, status_code = {"message": "Missing required fields"}, 400
    return response, status_code

  if not validate_mood_level(mood_level):
    response, status_code = {"message": "Invalid mood level"}, 400
    return response, status_code

  if not validate_hydration_level(hydration_level):
    response, status_code = {"message": "Invalid hydration level"}, 400
    return response, status_code

  if not validate_calories_intake(calories_intake):
    response, status_code = {"message": "Invalid calories intake"}, 400
    return response, status_code

  new_survey = Survey(
      member_id=member_id,
      mood_level=mood_level,
      hydration_level=hydration_level,
      calories_intake=calories_intake
  )
  new_survey.save()
  response, status_code = {"message": "Survey created successfully"}, 201

  return response, status_code


def get_user_survey(survey_id):
  survey = Survey.query.get_or_404(survey_id)
  response, status_code = survey.serialize(), 200
  return response, status_code


def update_user_survey(survey_id, data):
  survey = Survey.query.get_or_404(survey_id)

  if survey:
    survey.energy_level = data.get('energy_level', survey.energy_level)
    survey.mood_level = data.get('mood_level', survey.mood_level)
    survey.hydration_level = data.get(
        'hydration_level', survey.hydration_level)
    survey.calories_intake = data.get(
        'calories_intake', survey.calories_intake)
    survey.save()
    response, status_code = {"message": "Survey updated successfully"}, 200
  else:
    response, status_code = {"message": "Survey not found"}, 404

  return response, status_code


def delete_user_survey(survey_id):
  survey = Survey.query.get_or_404(survey_id)
  survey.delete()
  response, status_code = {"message": "Survey deleted successfully"}, 200
  return response, status_code
