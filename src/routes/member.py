from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

from ..services.member_services import get_member_settings, update_member_settings, delete_member

member_ns = Namespace('member', description='A namespace for Member')

member_model = member_ns.model(
    "Member", {
        "member_id": fields.Integer(description="The unique identifier of a member"),
        "email": fields.String(description="The email of the member"),
        "role_id": fields.Integer(description="The role of the member"),
        "join_date": fields.DateTime(description="The date the member joined"),
    }
)

member_settings_model = member_ns.model(
    "MemberSettings",
    {
        "member_id": fields.Integer(description="The unique identifier of a member"),
        "email": fields.String(description="The email of the member"),
        "role_id": fields.Integer(description="The role of the member"),
        "join_date": fields.DateTime(description="The date the member joined"),
        "first_name": fields.String(description="The first name of the member"),
        "last_name": fields.String(description="The last name of the member"),
        "username": fields.String(description="The username of the member"),
        "phone": fields.String(description="The phone number of the member"),
        "city": fields.String(description="The city of the member"),
        "state": fields.String(description="The state of the member"),
        "zip_code": fields.String(description="The zip code of the member"),
        "birthdate": fields.Date(description="The birthdate of the member"),
        "height": fields.Integer(description="The height of the member"),
        "weight": fields.Integer(description="The weight of the member"),
        "age": fields.Integer(description="The age of the member"),
        "gender": fields.String(description="The gender of the member")
    }
)

update_member_settings_model = member_ns.model(
    "MemberSettings",
    {
        "email": fields.String(description="The email of the member"),
        "first_name": fields.String(description="The first name of the member"),
        "last_name": fields.String(description="The last name of the member"),
        "username": fields.String(description="The username of the member"),
        "phone": fields.String(description="The phone number of the member"),
        "city": fields.String(description="The city of the member"),
        "state": fields.String(description="The state of the member"),
        "zip_code": fields.String(description="The zip code of the member"),
        "birthdate": fields.Date(description="The birthdate of the member"),
        "height": fields.Integer(description="The height of the member"),
        "weight": fields.Integer(description="The weight of the member"),
        "age": fields.Integer(description="The age of the member"),
        "gender": fields.String(description="The gender of the member")
    }
)


@member_ns.route('/settings')
@member_ns.response(404, 'Member not found.')
class MemberSettingsResource(Resource):
  @jwt_required()
  def get(self):
    """
    Retrieves the settings for the current logged-in member.
    :return: The settings of the current member.
    """
    result, status_code = get_member_settings()
    return make_response(jsonify(result), status_code)

  @member_ns.expect(update_member_settings_model)
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
