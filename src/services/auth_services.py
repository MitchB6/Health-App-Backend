from flask import jsonify
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity, jwt_required)

from ..models.member_model import Member
from ..models.password_model import Password
from ..models.coach_model import CoachInfo
from ..models.personalinfo_model import PersonalInfo
from ..extensions import db, bcrypt
from .validations import *


def create_coach(data):

  member_id = int(data.get('member_id'))
  specialization = str(data.get('specialization'))
  price = round(float(data.get('price')), 2)
  location = str(data.get('location'))
  schedule_general = str(data.get('schedule_general'))
  qualifications = str(data.get('qualifications'))
  approved = False

  if not specialization:
    return {"message": "Specialization cannot be empty"}, 400
  if not location:
    return {"message": "Location cannot be empty"}, 400
  if not qualifications:
    return {"message": "Qualifications cannot be empty"}, 400
  if not schedule_general:
    return {"message": "Schedule cannot be empty"}, 400
  if price < 0:
    return {"message": "Price cannot be negative"}, 400
  if not member_id:
    return {"message": "Member ID cannot be empty"}, 400

  if not Member.query.get(member_id):
    return {"message": "Member ID does not exist"}, 404

  existing_coach = CoachInfo.query.filter_by(member_id=member_id).first()
  if existing_coach:
    return {"message": "A coach with this Member ID already exists"}, 400

  new_CoachInfo = CoachInfo(
      member_id=member_id,
      specialization=specialization,
      price=price,
      location=location,
      schedule_general=schedule_general,
      qualifications=qualifications,
      approved=approved
  )

  CoachInfo.save(new_CoachInfo)

  return {"message": "Coach form submitted successfully"}, 200


def change_password(data):
  get_jwt_identity()
  current_member_id = get_jwt_identity()
  old_password = str(data.get('old_password'))
  new_password = str(data.get('new_password'))

  member = Member.query.get_or_404(current_member_id)
  current_password = member.passwords.hashed_pw

  if not bcrypt.check_password_hash(current_password, old_password):
    return {"message": "Old password is incorrect"}, 401

  hashed_new_password = bcrypt.generate_password_hash(new_password)
  member.passwords.hashed_pw = hashed_new_password
  db.session.commit()

  return {"message": "Password changed successfully"}, 200


def create_user(data):
  role_id = int(data.get('role_id'))
  username = str(data.get('username'))
  email = str(data.get('email'))
  password = str(data.get('password'))
  phone = str(data.get('phone'))

  if role_id == 2:
    return {"message": "Cannot signup as an admin"}, 400
  # Validate email
  if not validate_email(email):
    return {"message": "Invalid email format"}, 400
  if not validate_username(username):
    return {"message": "Invalid username format"}, 400
  if not validate_phone(phone):
    return {"message": "Invalid phone format"}, 400
  # Validate password
  if not validate_password(password):
    return {"message": "Password must be at least 8 characters long"}, 400

  # Check if email already exists
  if Member.query.filter_by(email=email).first():
    return {"message": f"Email {email} already exists"}, 409

  new_member = Member(role_id=role_id, email=email)
  db.session.add(new_member)
  db.session.flush()

  new_personal_info = PersonalInfo(
      member_id=new_member.member_id,
      username=username,
      phone=phone
  )
  db.session.add(new_personal_info)

  new_password = Password(
      member_id=new_member.member_id,
      hashed_pw=bcrypt.generate_password_hash(password)
  )
  db.session.add(new_password)
  db.session.commit()

  return {"message": f"User created successfully : {new_member.member_id}"}, 200


def login_user(data):
  role_id = int(data.get('role_id'))
  print(role_id)
  email = str(data.get('email'))
  password = str(data.get('password'))

  if not validate_email(email):
    return {"message": "Invalid email format"}, 400

  if not password:
    return {"message": "Password cannot be empty"}, 400

  if role_id not in [0, 1, 2]:
    return {"message": "Role ID empty or invalid"}, 400

  db_user = Member.query.filter_by(email=email).first()

  if not db_user:
    return {"message": "Email not found"}, 404

  if role_id != db_user.role_id:
    return {"message": "Invalid role selection"}, 400

  if db_user and bcrypt.check_password_hash(db_user.passwords.hashed_pw, password):
    access_token = create_access_token(
        identity=db_user.member_id, additional_claims={"role_id": db_user.role_id})
    refresh_token = create_refresh_token(
        identity=db_user.member_id, additional_claims={"role_id": db_user.role_id})

    return {
        "access token": access_token,
        "refresh token": refresh_token
    }, 200
  elif db_user:
    return {"message": "Wrong password"}, 401
  else:
    return {"message": "User not found"}, 404


def refresh_access_token():
  current_user = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user)
  return {"access_token": new_access_token}, 200
