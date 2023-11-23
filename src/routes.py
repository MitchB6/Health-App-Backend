from flask import jsonify,request
from flask_restx import Resource,fields
from .extensions import api,bcrypt
from .serializers import member_model, password_model
from .models import Member,Password

signup_model=api.model(
    "SignUp",
    {
        "email":fields.String,
        "password":fields.String()
    }
)

workout_model=api.model(
    "Workout",
    {
        "name":fields.String()
    }
)

member_model=api.model(
    "Member",
    {
        "first_name":fields.String(),
        "last_name":fields.String()
    }
)
    
@api.route('/')
class HomeResource(Resource):
    def get(self):
        return {"message":"Welcome to our fitness app"}

@api.route('/health')
class HealthResource(Resource):
  def get(self):
    """Health check of backend"""
    return {'status': 'success', 'message': 'Health check success'}

@api.route('/members/<int:id>')
class MemberResource(Resource):
    def get(self,id):
        """Get a member by id"""
        pass
    
    def put(self,id):
        """Update a member by id"""
        pass
    
    def delete(self,id):
        """Delete a member by id"""
        pass
    
@api.route('/signup')
class SignUp(Resource):
    @api.expect(signup_model)
    def post(self):
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
        new_member.commit()
        
        return jsonify({"message": "User created successfully"})
