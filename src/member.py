from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required

from .models import Member
from .serializers import member_model, member_ns

@member_ns.route('/member/<int:id>')
class MemberResource(Resource):
    @member_ns.marshal_with(member_model)
    def get(self,id):
        """Get a member by id"""
        member=Member.query.get_or_404(id)
        return member
    
    @member_ns.marshal_with(member_model)
    @jwt_required()
    def put(self,id):
        """Update a member by id"""
        member_to_update=Member.query.get_or_404(id)
        data=request.get_json()
        member_to_update.update(**data)
            
    @member_ns.marshal_with(member_model)
    def delete(self,id):
        """Delete a member by id"""
        recipe_to_delete=Member.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete