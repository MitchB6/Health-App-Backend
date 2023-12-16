from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.client_services import *
from ..services.decorators import coach_required

client_ns = Namespace('clients', description="A namespace for clients")


@client_ns.route('/')
class AllClients(Resource):
  @coach_required
  def get(self):
    """get all clients"""
    client_list, status_code = get_all_clients()
    return make_response(client_list, status_code)


@client_ns.route('/requests')
class ClientRequests(Resource):
  @coach_required
  def get(self):
    """Get all client requests"""
    request_list, status_code = get_client_requests()
    return make_response(request_list, status_code)


@client_ns.route('/accept_request/<int:link_id>')
class AcceptClientRequest(Resource):
  @coach_required
  def post(self, link_id):
    """Accept a client request"""
    response, status_code = accept_client_request(link_id)
    return make_response(response, status_code)


@client_ns.route('/decline_request/<int:link_id>')
class DeclineClientRequest(Resource):
  @coach_required
  def post(self, request_id):
    """Decline a client request"""
    response, status_code = decline_client_request(request_id)
    return make_response(response, status_code)


@client_ns.route('/client_dashboard/<int:member_id>')
class ClientDashboard(Resource):
  @coach_required
  def get(self, client_id):
    """Get a client's dashboard"""
    dashboard_data = get_client_dashboard(client_id)
    return make_response(dashboard_data, 200)
