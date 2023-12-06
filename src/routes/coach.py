from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.coach_services import *
from ..services.decorators import coach_required


coach_ns = Namespace('coaches', description="A namespace for coaches")

hire_request_model = coach_ns.model('HireRequest', {
    'client_name': fields.String(required=True, description='Client name'),
    'coach_id': fields.Integer(required=True, description='Coach ID'),
})


@coach_ns.route('/')
class AllCoaches(Resource):
  @jwt_required()
  def get(self):
    """Get all coaches."""
    result, status_code = get_all_coaches()
    return make_response(jsonify(result), status_code)


@coach_ns.route('/<int:coach_id>')
class CoachDetails(Resource):
  @jwt_required()
  def get(self, coach_id):
    """Get coach details by coach_id."""
    result, status_code = get_coach(coach_id)
    return make_response(jsonify(result), status_code)


@coach_ns.route('/request_hire')
class HireRequestResource(Resource):
  @coach_ns.expect(hire_request_model)
  def post(self):
    data = request.json()
    result, status_code = link_request(data)
    return make_response(jsonify(result), status_code)
