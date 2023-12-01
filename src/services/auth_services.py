from flask import jsonify
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity)

from ..models.member_model import Member
from ..models.password_model import Password
from ..models.coach_model import CoachInfo
from ..models.personalinfo_model import PersonalInfo
from ..extensions import db, bcrypt
from .validations import *


def create_coach(data):

    member_id = int(data.get('member_id'))
    specialization = str(data.get('specialization'))
    price = float(data.get('price'))
    location = str(data.get('location'))
    schedule_text = str(data.get('schedule_text'))
    qualifications = str(data.get('qualifications'))
    approved = False

    new_CoachInfo = CoachInfo(
        member_id=member_id,
        specialization=specialization,
        price=price,
        location=location,
        schedule_text=schedule_text,
        qualifications=qualifications,
        approved=approved
    )

    db.session.add(new_CoachInfo)

    return {"message": "Coach form submitted successfully"}, 200


def update_coach(data):
    approved = bool(data.get('approved'))
    if approved:
        coach = CoachInfo.query.get_or_404(data.get('coach_id'))
        coach.approved = approved
        db.session.commit()
        return {"message": "Coach approved"}, 200
    else:
        coach = CoachInfo.query.get_or_404(data.get('coach_id'))
        db.CoachInfo.delete(coach)
        return {"message": "Coach denied"}, 200


def get_all_coach_forms():
    forms = CoachInfo.query.filter_by(approved=False).all()
    return jsonify([form.serialize() for form in forms]), 200


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
        return {"message": "Invalid credentials"}, 401
    else:
        return {"message": "User not found"}, 404


def refresh_access_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return {"access_token": new_access_token}, 200