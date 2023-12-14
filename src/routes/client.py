from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.client_services import *
from ..services.decorators import coach_required

client_ns = Namespace('clients', description="A namespace for clients")


@client_ns.route('/')
class AllClients(Resource):
  @jwt_required()
  @coach_required
  def get(self):
    """Get all clients."""
    client_list = get_all_clients()
    return make_response(client_list, 200)


@client_ns.route('/<int:client_id>')
class ClientResource(Resource):
  @jwt_required()
  def get(self, client_id):
    """Get a specific client."""

    return make_response(response_from_services, 200)

  def delete(self, client_id):
    """Delete a specific client."""
    return make_response()
