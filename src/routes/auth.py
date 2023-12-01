from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required

from ..services.auth_services import *
from ..services.decorators import admin_required

auth_ns = Namespace('auth', description="A namespace for Authentication")

specializations = ['Weight Loss', 'Weight Gain', 'Body Building',
                   'General Fitness', 'Yoga', 'Pilates', 'Crossfit',]
schedules = ['Weekdays', 'Weekends', 'Weekdays and Weekends']
qualifications = ['ACE', 'ACSM', 'NASM', 'ISSA', 'NSCA', 'NCSF',
                  'NCCPT', 'NESTA', 'NCSM', 'NFPT', 'Cooper Institute', 'Other']

coach_signup_model = auth_ns.model(
    "CoachSignUp",
    {
        "specialization": fields.String(required=True, default_specialization=specializations[0]),
        "price": fields.Float(required=True, default=0.0),
        "location": fields.String(required=True),
        "schedule_text": fields.String(required=True, general_schedule=schedules[0]),
        "qualifications": fields.String(required=True, default_qualifications=qualifications[0]),
        "member_id": fields.Integer(required=True)
    }
)

signup_model = auth_ns.model(
    "SignUp",
    {
        "role_id": fields.Integer(required=True, default=0),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "phone": fields.String(required=False)
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "role_id": fields.Integer(default=0, required=True),
        "email": fields.String(default="bill@email.com", required=True),
        "password": fields.String(default="12345678", required=True)
    }
)

change_password_model = auth_ns.model(
    "ChangePassword",
    {
        "old_password": fields.String(default="12345678", required=True),
        "new_password": fields.String(default="password", required=True)
    }
)


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
    data = request.get_json()
    result, status_code = create_user(data)
    return make_response(jsonify(result), status_code)


@auth_ns.route('/coach_signup')
class CoachSignUp(Resource):
  @auth_ns.expect(coach_signup_model)
  def post(self):
    """Coach form submission"""
    data = request.get_json()
    result, status_code = create_coach(data)
    return make_response(jsonify(result), status_code)

  @jwt_required()
  @admin_required
  def get(self):
    """Get all coach forms"""
    result, status_code = get_all_coach_forms()
    return make_response(jsonify(result), status_code)

  @jwt_required()
  @admin_required
  def put(self):
    """Approve coach form"""
    data = request.get_json()
    result, status_code = update_coach(data)
    return make_response(jsonify(result), status_code)


@auth_ns.route('/login')
class Login(Resource):
  @auth_ns.expect(login_model)
  @auth_ns.doc(responses={
      200: 'Success',
      400: 'Missing required fields',
      401: 'Invalid credentials',
      409: 'User does not exist'
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
