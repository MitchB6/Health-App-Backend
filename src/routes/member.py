from flask_restx import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

from ..services.member_services import get_member_settings, update_member_settings, delete_member
from ..serializers.member_serializer import member_model
from ..namespace import member_ns

@member_ns.route('/settings')
class MemberSettingsResource(Resource):
  @member_ns.marshal_with(member_model)
  @member_ns.expect(security='Bearer Auth')
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
  @member_ns.expect(member_model, security='Bearer Auth')
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
  @member_ns.expect(security='Bearer Auth')
  def delete(self):
    """
    Deletes the current logged-in member.
    :return: Success message.
    """
    result, status_code = delete_member()
    return make_response(jsonify(result), status_code)
