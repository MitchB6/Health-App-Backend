from flask_restx import Resource
from flask import request, jsonify
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
    return get_member_settings()

  @member_ns.marshal_with(member_model)
  @member_ns.expect(member_model, security='Bearer Auth')
  @jwt_required()
  def put(self):
    """
    Updates the settings for the current logged-in member.
    :return: The updated member data.
    """
    data = request.get_json()
    return update_member_settings(data), 200

  @jwt_required()
  @member_ns.expect(security='Bearer Auth')
  def delete(self):
    """
    Deletes the current logged-in member.
    :return: Success message.
    """
    return jsonify(delete_member()), 200
