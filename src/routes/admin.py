from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.admin_services import get_all_coach_forms, update_coach
from ..services.decorators import admin_required

admin_ns = Namespace('admin', description='A namespace for Admin')

coach_approval_model = admin_ns.model(
    "CoachApproval",
    {
        "coach_id": fields.Integer(required=True),
        "approved": fields.Boolean(required=True)
    }
)


@admin_ns.route('/')
class AdminResource(Resource):
  @jwt_required()
  @admin_required
  def get(self):
    """Get all coach forms"""
    result, status_code = get_all_coach_forms()
    return make_response(jsonify(result), status_code)

  @jwt_required()
  @admin_required
  @admin_ns.expect(coach_approval_model)
  def put(self):
    """Approve coach form"""
    data = request.get_json()
    result, status_code = update_coach(data)
    return make_response(jsonify(result), status_code)
