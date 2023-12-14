from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.coach_services import *
from ..services.decorators import coach_required


coach_ns = Namespace('coaches', description="A namespace for coaches")

hire_request_model = coach_ns.model('HireRequest', {
    'member_id': fields.String(required=True, description='Client name'),
    'coach_id': fields.Integer(required=True, description='Coach ID'),
})


@coach_ns.route('/')
class AllCoaches(Resource):
  @jwt_required() #the login token
  @coach_ns.doc(params={'specialization': 'Specialization of coach',
                        'price': 'Price of coach',
                        'location': 'Location of coach'})
  def get(self):
    """Get all coaches."""
    specialization = request.args.get('specialization', None)
    price = request.args.get('price', None)
    location = request.args.get('location', None)
    result, status_code = search_coaches(specialization, price, location)
    return make_response(jsonify(result), status_code)


@coach_ns.route('/request_hire')
class HireRequestResource(Resource):
  @coach_ns.expect(hire_request_model)
  def post(self):
    """Request to hire a coach."""
    data = request.json
    result, status_code = link_request(data)
    return make_response(jsonify(result), status_code)
