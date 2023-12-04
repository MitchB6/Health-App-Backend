# decorators.py
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required
from functools import wraps
from flask import jsonify


def admin_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    verify_jwt_in_request()
    claims = get_jwt()
    if claims.get("role_id") != 2:
      return {"message": "Admins only!"}, 403
    return fn(*args, **kwargs)

  return wrapper


def coach_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    verify_jwt_in_request()
    claims = get_jwt()
    if claims.get("role_id") != 1:
      return {"message": "Coaches only!"}, 403
    return fn(*args, **kwargs)


def jwt_required_custom(fn):
  @jwt_required()
  def wrapper(*args, **kwargs):
    try:
      verify_jwt_in_request()
      return fn(*args, **kwargs)
    except Exception as e:
      return {"message": "JWT validation error: " + str(e)}, 401

  return wrapper
