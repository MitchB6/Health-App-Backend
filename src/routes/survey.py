from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

from ..services.survey_services import *

survey_ns = Namespace('survey', description='A namespace for User Survey')

survey_model = survey_ns.model(
    "UserSurvey", {
        "survey_id": fields.Integer(description="The unique identifier of a survey"),
        "member_id": fields.Integer(description="The member ID associated with the survey"),
        "date": fields.DateTime(description="The date of the survey"),
        "energy_level": fields.Integer(description="Energy level reported in the survey"),
        "mood_level": fields.Integer(description="Mood level reported in the survey"),
        "hydration_level": fields.Float(description="Hydration level reported in the survey"),
        "calories_intake": fields.Integer(description="Calories intake reported in the survey"),
        "recorded_at": fields.DateTime(description="The date and time the survey was recorded"),
    }
)


@survey_ns.route('/')
class SurveyResource(Resource):
  @jwt_required()
  def get(self):
    """
    Retrieves the surveys for the current logged-in member.
    :return: The surveys of the current member.
    """
    result, status_code = get_user_survey()
    return make_response(jsonify(result), status_code)

  @survey_ns.expect(survey_model)
  @jwt_required()
  def post(self):
    """
    Creates a new user survey entry.
    :return: The created survey data.
    """
    data = request.get_json()
    result, status_code = create_user_survey(data)
    return make_response(jsonify(result), status_code)


@survey_ns.route('/<int:survey_id>')
class SurveyDetailResource(Resource):
  @jwt_required()
  def get(self, survey_id):
    """
    Retrieves details of a specific user survey.
    :param survey_id: The ID of the survey to retrieve.
    :return: The details of the survey.
    """
    result, status_code = get_user_survey(survey_id)
    return make_response(jsonify(result), status_code)

  @survey_ns.expect(survey_model)
  @jwt_required()
  def put(self, survey_id):
    """
    Updates the details of a specific user survey.
    :param survey_id: The ID of the survey to update.
    :return: The updated survey data.
    """
    data = request.get_json()
    result, status_code = update_user_survey(survey_id, data)
    return make_response(jsonify(result), status_code)

  @jwt_required()
  def delete(self, survey_id):
    """
    Deletes a specific user survey.
    :param survey_id: The ID of the survey to delete.
    :return: Success message.
    """
    result, status_code = delete_user_survey(survey_id)
    return make_response(jsonify(result), status_code)
