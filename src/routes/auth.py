from flask import jsonify,request,make_response
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from ..serializers.auth_serializer import *
from ..services.auth_services import *
from ..namespace import auth_ns

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.doc(responses={
      200: 'Success',
      400: 'Invalid input',
      409: 'Email already exists'
    })
    def post(self):
      """User signup with email and password"""
      data=request.get_json()
      result, status_code = create_user(data)
      return make_response(jsonify(result), status_code)
    
@auth_ns.route('/login')
class Login(Resource):
  @auth_ns.expect(login_model)
  @auth_ns.doc(responses={
    200: 'Success',
    401: 'Invalid credentials'
  })
  def post(self):
    """User login using email and password"""
    data = request.get_json()
    result, status_code = login_user(data)
    return make_response(jsonify(result), status_code)

@auth_ns.route('/refresh')
class RefreshResource(Resource):
  @auth_ns.expect(security='Bearer Auth')
  @jwt_required(refresh=True)
  def post(self):
    """User gets new access token with refresh token"""
    result, status_code = refresh_access_token()
    return make_response(jsonify(result), status_code)

@auth_ns.route('/change_password')
class ChangePasswordResource(Resource):
  @auth_ns.expect(change_password_model, security='Bearer Auth')
  @auth_ns.doc(responses={
    200: 'Success',
    401: 'Invalid credentials'
  })
  @jwt_required()
  def post(self):
    """Endpoint for a member to change their password"""
    data = request.get_json()
    
    result, status_code = change_password(data)
    return make_response(jsonify(result), status_code)