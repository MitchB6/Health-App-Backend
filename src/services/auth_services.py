from flask import jsonify
from flask_jwt_extended import (JWTManager, create_access_token,
create_refresh_token,get_jwt_identity)

from ..models.member_model import Member
from ..models.password_model import Password
from ..models.personalinfo_model import PersonalInfo
from ..extensions import db, bcrypt
from .validations import *

def change_password(data):
  get_jwt_identity()
  current_member_id = get_jwt_identity()
  old_password = data.get('old_password')
  new_password = data.get('new_password')
  
  member = Member.query.get_or_404(current_member_id)
  current_password = member.passwords.hashed_pw

  if not bcrypt.check_password_hash(current_password, old_password):
    return {"message": "Old password is incorrect"}, 401

  hashed_new_password = bcrypt.generate_password_hash(new_password)
  member.passwords.hashed_pw = hashed_new_password
  db.session.commit()

  return {"message": "Password changed successfully"}, 200

def create_user(data):
  role_id=data.get('role_id')
  username=data.get('username')
  email=data.get('email')
  password=data.get('password')
  phone=data.get('phone')
  
  if role_id==2:
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
  
  new_member = Member(role_id=role_id,email=email)
  db.session.add(new_member)
  db.session.flush()  # Flush to get member_id

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

  return {"message": "User created successfully"}, 201

def login_user(data):
  role_id=data.get('role_id')
  email=data.get('email')
  password=data.get('password')
  
  if not validate_email(email):
    return {"message": "Invalid email format"}, 400

  if not password:
    return {"message": "Password cannot be empty"}, 400

  if role_id==2:
    return {"message": "Cannot login as an admin"}, 400
  
  if int(role_id) in [0,1]:
    user = Member.query.filter_by(email=email).first()

  db_user = Member.query.filter_by(email=email).first()
  if db_user and bcrypt.check_password_hash(db_user.passwords.hashed_pw, password):
    access_token = create_access_token(identity=db_user.member_id,additional_claims={"role_id": user.role_id})
    refresh_token = create_refresh_token(identity=db_user.member_id, additional_claims={"role_id": user.role_id})

    return {
      "access token": access_token,
      "refresh token": refresh_token
    }, 200
  elif db_user:
    return {"message": "Invalid credentials"}, 401
  else:
    return {"message": "User not found"}, 404

def refresh_access_token():
  current_user = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user)
  return {"access_token": new_access_token}, 200