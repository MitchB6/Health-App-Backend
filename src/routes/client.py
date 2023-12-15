from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.client_services import *
from ..services.decorators import coach_required

client_ns = Namespace('clients', description="A namespace for clients")

@client_ns.route('/')
class AllClients(Resource):
    @jwt_required
    @coach_required
    def get(self):
        """get all cleints"""
        client_list = get_all_clients()
        return make_response(client_list, 200)

@client_ns.route('/accept_request/<int:request_id>')
class AcceptClientRequest(Resource):
    @jwt_required
    @coach_required
    def post(self, request_id):
        """Accept a client request"""
        response, status_code = accept_client_request(request_id)
        return make_response(jsonify(response), status_code)

@client_ns.route('/decline_request/<int:request_id>')
class DeclineClientRequest(Resource):
    @jwt_required
    @coach_required
    def post(self, request_id):
        """Decline a client request"""
        response, status_code = decline_client_request(request_id)
        return make_response(jsonify(response), status_code)

@client_ns.route('/client_dashboard/<int:client_id>')
class ClientDashboard(Resource):
    @jwt_required
    @coach_required
    def get(self, client_id):
        """Get a client's dashboard"""
        dashboard_data = get_client_dashboard(client_id)
        return make_response(jsonify(dashboard_data), 200)

@client_ns.route('/create_workout_plan')
class CreateWorkoutPlan(Resource):
    @jwt_required
    @coach_required
    def post(self):
        """Create a personalized workout plan for client"""
        data = request.json
        response, status_code = create_workout_plan(data['member_id'], data['workout_details'])
        return make_response(jsonify(response), status_code)