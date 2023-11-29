from flask_jwt_extended import get_jwt_identity
import re #regex

from ..models.member_model import Member
from .validations import *

def get_member_settings():
    current_member_id = get_jwt_identity()
    if current_member_id is None:
        return {"message": "Member not found."}
    member = Member.query.get_or_404(current_member_id)
    return member, 200

def update_member_settings(data):
    current_member_id = get_jwt_identity()
    member = Member.query.get_or_404(current_member_id)
    member.update(**data)
    return {"message": "Member settings updated successfully."}, 200

def delete_member():
    current_member_id = get_jwt_identity()
    member = Member.query.filter_by(member_id=current_member_id).first_or_404()
    member.delete()
    return {"message": "Member deleted successfully."}, 200
