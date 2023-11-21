from flask_restx import Resource
from .extensions import api
from .serializers import member_model
from .models import Member

@api.route('/members')
class MembersResource(Resource):
    @api.marshal_list_with(member_model)
    def get(self):
        """Get all members"""
        members = Member.query.all()

        return members
    
    @api.marshal_with(member_model)
    def post(self):
        """Create a new member"""
        pass

@api.route('/recipe/<int:id>')
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