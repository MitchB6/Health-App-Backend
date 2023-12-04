from flask import jsonify
from flask_restx import Resource

from .serializers import home_ns

@home_ns.route('/')
class HomeResource(Resource):
    def get(self):
        """Homepage"""
        return jsonify({"message":"hello world"})

@home_ns.route('/health')
class HealthResource(Resource):
  def get(self):
    """Health check of backend"""
    return jsonify({'status': 'success', 'message': 'Health check success'})
        