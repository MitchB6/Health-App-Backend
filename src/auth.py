from flask import jsonify,request,make_response
from flask_restx import Resource
from flask_jwt_extended import (JWTManager, create_access_token,
create_refresh_token,jwt_required,get_jwt_identity)

from .extensions import bcrypt
from .serializers import signup_model,login_model,auth_ns
from .models import Member,Password

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        """User signup with email and password"""
        data=request.get_json()
        email=data.get('email')
        
        db_user=Member.query.filter_by(email=email).first()
        if db_user is not None:
            return jsonify({"message":f"Email {email} already exists"})
        
        new_member=Member(
            email=data.get('email')
        )
        new_member.save(flush=True)
        new_password=Password(
            member_id=new_member.member_id,
            hashed_pw=bcrypt.generate_password_hash(data.get('password'))
        )
        new_password.save()
        new_member.save(commit=True)
        
        return jsonify({"message": "User created successfully"})
    
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """User login using email and password"""
        data=request.get_json()
        

        email=data.get('email')

        password=data.get('password')
        print("Line47")
        db_user=Member.query.filter_by(email=email).first()
        print("Line49")
        if db_user:
            db_password = db_user.passwords
            print("Line52")
            if db_user and bcrypt.check_password_hash(db_password.hashed_pw, password):
                print("Line54")                
                access_token=create_access_token(identity=db_user.member_id)
                refresh_token=create_refresh_token(identity=db_user.member_id)
                
                print("Access Token:", access_token)
                print("Refresh Token:", refresh_token)
                
                response_data={
                    "access token": access_token,
                    "refresh token": refresh_token
                }
                print("Response Data:", response_data)
                return jsonify(response_data)
            else:
                return jsonify({"message":"Invalid credentials"}), 401
        else:
            return jsonify({"message": "User not found"}), 404


@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        
        current_user=get_jwt_identity()
        
        new_access_token=create_access_token(identity=current_user)
        
        return make_response(jsonify({"access_token":new_access_token}),200)