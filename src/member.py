from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required

from .models import Member
from .serializers import member_model, member_ns

@member_ns.route('/member/<int:id>')
class MemberResource(Resource):
    @member_ns.marshal_with(member_model)
    def get(self,id):
        """
        The function `get` retrieves a member from the database based on their id and returns it.
        
        :param id: The id parameter is the unique identifier of the member that we want to retrieve from the
        database
        :return: The member object with the specified id is being returned.
        """
        member=Member.query.get_or_404(id)
        return member
    
    @member_ns.marshal_with(member_model)
    @jwt_required()
    def put(self,id):
        """
        The `put` function updates a member in the database based on their ID.
        
        :param id: The `id` parameter is the unique identifier of the member that needs to be updated
        """
        member_to_update=Member.query.get_or_404(id)
        data=request.get_json()
        member_to_update.update(**data)
            
    @member_ns.marshal_with(member_model)
    def delete(self,id):
        """
        The above function deletes a recipe with a given ID from the database and returns the deleted
        recipe.
        
        :param id: The `id` parameter is the unique identifier of the recipe that needs to be deleted
        :return: The recipe that was deleted is being returned.
        """
        recipe_to_delete=Member.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete