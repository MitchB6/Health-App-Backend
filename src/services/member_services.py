from flask_jwt_extended import get_jwt_identity
import re  # regex

from ..models.member_model import Member
from ..models.goals_model import MemberGoals
from ..models.personalinfo_model import PersonalInfo
from ..extensions import db
from ..services.validations import *


def marshal_membersettings(member, personal_info):
  return {
      "member_id": member.member_id,
      "email": member.email,
      "role_id": member.role_id,
      "join_date": member.join_date.strftime('%Y-%m-%d') if member.join_date else None,
      "first_name": personal_info.first_name,
      "last_name": personal_info.last_name,
      "username": personal_info.username,
      "phone": personal_info.phone,
      "city": personal_info.city,
      "state": personal_info.state,
      "zip_code": personal_info.zip_code,
      "birthdate": personal_info.birthdate.strftime('%Y-%m-%d') if personal_info.birthdate else None,
      "height": personal_info.height,
      "weight": personal_info.weight,
      "age": personal_info.age,
      "gender": personal_info.gender,
  }


def get_member_settings():
  current_member_id = get_jwt_identity()
  member_info = db.session.query(Member, PersonalInfo). \
      filter(Member.member_id == current_member_id). \
      outerjoin(PersonalInfo, Member.member_id ==
                PersonalInfo.member_id).first()

  member, personal_info = member_info

  if not member:
    return {"message": "Member not found."}, 404

  response = marshal_membersettings(member, personal_info)

  return response, 200


def update_member_settings(data):
  member_id = get_jwt_identity()
  member = Member.query.get_or_404(member_id)

  allowed_fields_member = ['email']
  allowed_fields_personal_info = ['username', 'phone', 'first_name', 'last_name', 'city', 'state', 'zip_code',
                                  'birthdate', 'height', 'weight', 'age', 'gender']

  validation_functions = {
      'email': validate_email,
      'phone': validate_phone,
      'first_name': validate_first_name,
      'last_name': validate_last_name,
      'city': validate_city,
      'state': validate_state,
      'zip_code': validate_zip_code,
      'birthdate': validate_birthdate,
      'height': validate_height,
      'weight': validate_weight,
      # Add other validations as needed
  }

  for key, value in data.items():
    if key in allowed_fields_member + allowed_fields_personal_info and value is not None:
      if key in validation_functions and not validation_functions[key](value):
        return {"message": f"Invalid {key}"}, 400
      if key in allowed_fields_member:
        setattr(member, key, value)
      elif key in allowed_fields_personal_info:
        setattr(member.personal_info, key, value)
  db.session.commit()
  return {"message": "Member settings updated successfully."}, 200


def delete_member():
  member_id = get_jwt_identity()
  member = Member.query.filter_by(member_id=member_id).first_or_404()
  member.delete()
  return {"message": "Member deleted successfully."}, 200


def get_member_goals():
  member_id = get_jwt_identity()
  goals = MemberGoals.query.filter_by(member_id=member_id).first_or_404()

  if goals:
    serialized_goals = [goal.serialize() for goal in goals]
    return serialized_goals, 200
  else:
    return {"message": "No goals found"}, 404


def create_member_goal(goal_details):
  member_id = get_jwt_identity()
  new_goal = MemberGoals(
      member_id=member_id, **goal_details)
  db.session.add(new_goal)
  db.session.flush()
  db.session.commit()
  return {"message": f"Goal created successfully : {new_goal}"}, 404


def get_member_workouts():
  member_id = get_jwt_identity()
  workouts = Member.query.filter_by(member_id=member_id).first_or_404()

  if workouts:
    serialized_workouts = [workout.serialize() for workout in workouts]
    return serialized_workouts, 200
  else:
    return {"message": "No workouts found"}, 404
