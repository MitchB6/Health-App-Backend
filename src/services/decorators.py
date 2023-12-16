# decorators.py
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required
from functools import wraps


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

  return wrapper
