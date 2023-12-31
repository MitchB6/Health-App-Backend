from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.coach_services import *


coach_ns = Namespace('coaches', description="A namespace for coaches")

specializations = ['Weight Loss', 'Weight Gain', 'Body Building',
                   'General Fitness', 'Yoga', 'Pilates', 'Crossfit',]
schedules = ['Weekdays', 'Weekends', 'Weekdays and Weekends']
qualifications = ['ACE', 'ACSM', 'NASM', 'ISSA', 'NSCA', 'NCSF',
                  'NCCPT', 'NESTA', 'NCSM', 'NFPT', 'Cooper Institute', 'Other']

hire_request_model = coach_ns.model('HireRequest', {
    'member_id': fields.Integer(required=True, description='Client ID'),
    'coach_id': fields.Integer(required=True, description='Coach ID'),
})


@coach_ns.route('/')
class AllCoaches(Resource):
  @jwt_required()
  @coach_ns.doc(params={'specialization': 'Specialization of coach',
                        'price': 'Price of coach',
                        'location': 'Location of coach'})
  def get(self):
    """
    Get all coaches.
    GOOD
    """
    specialization = request.args.get('specialization', None)
    price = request.args.get('price', None)
    location = request.args.get('location', None)
    result, status_code = search_coaches(specialization, price, location)
    return make_response(jsonify(result), status_code)


@coach_ns.route('/request_hire <int:coach_id>')
class HireRequestResource(Resource):
  @jwt_required()
  def post(self, coach_id):
    """
    Request to hire a coach.
    GOOD
    """
    result, status_code = link_request(coach_id)
    return make_response(jsonify(result), status_code)
