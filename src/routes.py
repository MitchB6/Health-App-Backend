from flask import jsonify
from flask_restx import Resource

from .extensions import api

@api.route('/')
class HomeResource(Resource):
    def get(self):
        """Homepage"""
        return jsonify(message="hello world")

@api.route('/health')
class HealthResource(Resource):
  def get(self):
    """Health check of backend"""
    return jsonify({'status': 'success', 'message': 'Health check success'})
        