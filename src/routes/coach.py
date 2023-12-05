from flask import jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.coach_services import *
from ..services.decorators import coach_required

coach_ns = Namespace('coaches', description="A namespace for coaches")


@coach_ns.route('/coaches')
class AllCoaches(Resource):
  @jwt_required()
  def get(self):
    """Get all coaches."""
    current_user = get_jwt_identity()
    result, status_code = get_all_coaches()
    return make_response(jsonify(result), status_code)


@coach_ns.route('/coaches/<int:coach_id>')
class CoachDetails(Resource):
  @jwt_required()
  def get(self, coach_id):
    """Get coach details by coach_id."""
    current_user = get_jwt_identity()

    if current_user.get('role_id') != 1:
      return {"message": "Unauthorized"}, 403

    result, status_code = get_coach(coach_id)
    return make_response(jsonify(result), status_code)
