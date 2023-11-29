from flask import jsonify,request,make_response
from flask_restx import Resource, Namespace
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity

from ..serializers.auth_serializer import signup_model,login_model
from ..services.auth_services import create_user, login_user, refresh_access_token, change_password
from ..namespace import auth_ns


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
      """User signup with email and password"""
      data=request.get_json()
      result, status_code = create_user(data)
      return make_response(jsonify(result), status_code)
    
@auth_ns.route('/login')
class Login(Resource):
  @auth_ns.expect(login_model)
  def post(self):
    """User login using email and password"""
    data = request.get_json()
    result, status_code = login_user(data.get('email'), data.get('password'))
    return make_response(jsonify(result), status_code)

@auth_ns.route('/refresh')
class RefreshResource(Resource):
  @jwt_required(refresh=True)
  def post(self):
    """User gets new access token with refresh token"""
    result, status_code = refresh_access_token()
    return make_response(jsonify(result), status_code)

@auth_ns.route('/change_password')
class ChangePasswordResource(Resource):
  @jwt_required()
  def post(self):
    """Endpoint for a member to change their password"""
    current_member_id = get_jwt_identity()
    data = request.get_json()
   
    result, status_code = change_password(current_member_id, data.get('old_password'), data.get('new_password'))
    return make_response(jsonify(result), status_code)