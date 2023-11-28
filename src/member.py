from flask_restx import Resource
from flask import request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from .models import Member
from .serializers import member_model, member_ns


@member_ns.route('/<int:id>')
class MemberSettingsResource(Resource):
  @member_ns.marshal_with(member_model)
  def get(self):
    """
    Retrieves the settings for the current logged-in member.
    :return: The settings of the current member.
    """
    current_member_id =  get_jwt_identity()
    member=Member.query.get_or_404(current_member_id)
    return member
  
  @member_ns.marshal_with(member_model)
  @jwt_required()
  def put(self):
    """
    Updates the settings for the current logged-in member.
    :return: The updated member data.
    """
    current_member_id =  get_jwt_identity()
    member=Member.query.get_or_404(current_member_id)
    data=request.get_json()
    member.update(**data)
    return member, 200
            
  def delete(self,id):
    current_member_id =  get_jwt_identity()
    member=Member.query.filter_by(id=current_member_id, is_active=True).first_or_404()
    member.delete()
    return jsonify({"message": "Member deleted successfully.."}), 200

@member_ns.route('/<int:id>/goals')
class MemberGoalsResource(Resource):
  @member_ns.marshal_with(member_model)
  def get(self):
    """
    Retrieves the goals for the current logged-in member.
    :return: The goals of the current member.
    """
    current_member_id =  get_jwt_identity()
    member=Member.query.get_or_404(current_member_id)
    return member
  
  @member_ns.marshal_with(member_model)
  @jwt_required()
  def put(self):
    """
    Updates the goals for the current logged-in member.
    :return: The updated member data.
    """
    current_member_id =  get_jwt_identity()
    member=Member.query.get_or_404(current_member_id)
    data=request.get_json()
    member.update(**data)
    return member, 200

@member_ns.route('/<int:id>/workouts')
class WorkoutsResource(Resource):
  @member_ns.marshal_with(member_model)
  def get(self):
    """
    Retrieves the workouts for the current logged-in member.
    :return: The workouts of the current member.
    """
    current_member_id =  get_jwt_identity()
    member=Member.query.get_or_404(current_member_id)
    return member
  
  @member_ns.marshal_with(member_model)
  @jwt_required()
  def put(self):
    """
    Updates the workouts for the current logged-in member.
    :return: The updated member data.
    """
    current_member_id =  get_jwt_identity()
    member=Member.query.get_or_404(current_member_id)
    data=request.get_json()
    member.update(**data)
    return member, 200

