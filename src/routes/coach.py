from flask import request, make_response
from flask_restx import Resource, Namespace, fields

from ..services.coach_services import *

coach_ns = Namespace('coaches', description="A namespace for coaches")

coach_model = coach_ns.model(
    "Coach",
    {
        "specialization": fields.String(required=True),
        "price": fields.Float(required=True),
        "location": fields.String(required=True),
        "schedule_text": fields.String(required=True),
        "qualifications": fields.String(required=True),
        "member_id": fields.Integer(required=True)
    }
)


@coach_ns.route('/')
class CoachList(Resource):
    def get(self):
        """Get a list of all registered coaches."""
        result, status_code = get_all_coaches()
        return make_response(result, status_code)

    @coach_ns.expect(coach_model)
    def post(self):
        """Create a new coach."""
        data = request.json
        result, status_code = create_coach(data)
        return make_response(result, status_code)


@coach_ns.route('/<int:coach_id>')
class Coach(Resource):
    def get(self, coach_id):
        """Get details of a specific coach by coach_id."""
        result, status_code = get_coach(coach_id)
        return make_response(result, status_code)


@app.route('/coaches', methods=['GET'])
def get_all_coaches_route():
    result, status_code = get_all_coaches()
    return make_response(result, status_code)


@app.route('/coaches/<int:coach_id>', methods=['GET'])
def get_coach_route(coach_id):
    result, status_code = get_coach(coach_id)
    return make_response(result, status_code)


@app.route('/coaches', methods=['POST'])
def create_coach_route():
    data = request.json
    result, status_code = create_coach(data)
    return make_response(result, status_code)


@app.route('/coaches/<int:coach_id>', methods=['PUT'])
def update_coach_route(coach_id):
    data = request.json
    result, status_code = update_coach(coach_id, data)
    return make_response(result, status_code)
