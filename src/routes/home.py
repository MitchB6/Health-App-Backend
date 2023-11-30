from flask import jsonify
from flask_restx import Resource, Namespace

home_ns=Namespace('home',description='A namespace for Home')

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
        