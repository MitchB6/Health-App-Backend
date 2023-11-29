from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity

from ..models.personalinfo_model import PersonalInfo
from .validations import *

def get_member_settings():
  current_member_id = get_jwt_identity()
  if current_member_id is None:
    return {"message": "Member not found."}
  result, status_code = PersonalInfo.query.get_or_404(current_member_id)
  return make_response(jsonify(result, status_code))

def update_member_settings(data):
  current_member_id = get_jwt_identity()
  member = PersonalInfo.query.get_or_404(current_member_id)
  result, status_code = member.update(**data)
  return {"message": "Member settings updated successfully."}, 200

def delete_member():
  current_member_id = get_jwt_identity()
  member = PersonalInfo.query.filter_by(member_id=current_member_id).first_or_404()
  member.delete()
  return {"message": "Member deleted successfully."}, 200
