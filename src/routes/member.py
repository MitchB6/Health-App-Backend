from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

from ..services.member_services import get_member_settings, update_member_settings, delete_member

member_ns = Namespace('member', description='A namespace for Member')

member_model = member_ns.model(
    "Member",
    {
        "member_id": fields.Integer(description="The unique identifier of a member"),
        "username": fields.String(required=True, description="Member's username"),
        "first_name": fields.String(required=True, description="Member's first name"),
        "last_name": fields.String(required=True, description="Member's last name"),
        "email": fields.String(required=True, description="Member's email address"),
        "phone": fields.String(description="Member's phone number"),
        "role_id": fields.Integer(description="0 for user, 1 for coach, 2 for admin"),
        "city": fields.String(description="Member's city"),
        "state": fields.String(description="Member's state"),
        "zip_code": fields.String(description="Member's zip code"),
        "join_date": fields.DateTime(dt_format='rfc822', description="Date when the member joined"),
        "birthdate": fields.Date(description="Member's birthdate"),
        "height": fields.Integer(description="Member's height in centimeters"),
        "weight": fields.Integer(description="Member's weight in kilograms"),
        "age": fields.Integer(description="Member's age"),
        "gender": fields.String(description="Member's gender")
    }
)


@member_ns.route('/settings')
class MemberSettingsResource(Resource):
  @member_ns.marshal_with(member_model)
  @jwt_required()
  def get(self):
    """
    Retrieves the settings for the current logged-in member.
    :return: The settings of the current member.
    """
    print("GETTING MEMBER SETTINGS")
    result, status_code = get_member_settings()
    return make_response(jsonify(result), status_code)

  @member_ns.marshal_with(member_model)
  @member_ns.expect(member_model)
  @jwt_required()
  def put(self):
    """
    Updates the settings for the current logged-in member.
    :return: The updated member data.
    """
    data = request.get_json()
    result, status_code = update_member_settings(data)
    return make_response(jsonify(result), status_code)

  @jwt_required()
  def delete(self):
    """
    Deletes the current logged-in member.
    :return: Success message.
    """
    result, status_code = delete_member()
    return make_response(jsonify(result), status_code)
