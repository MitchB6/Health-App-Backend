from flask_jwt_extended import get_jwt_identity
import re #regex

from ..models.member_model import Member
from .validations import (validate_email, validate_password, validate_phone, 
validate_height, validate_weight, validate_zip_code, validate_state, validate_city, 
validate_birthdate, validate_username, validate_first_name, validate_last_name)

def get_member_settings():
    current_member_id = get_jwt_identity()
    if current_member_id is None:
        return {"message": "Member not found."}
    return Member.query.get_or_404(current_member_id)

def update_member_settings(data):
    current_member_id = get_jwt_identity()
    member = Member.query.get_or_404(current_member_id)
    return member.update(**data)

def delete_member():
    current_member_id = get_jwt_identity()
    member = Member.query.filter_by(id=current_member_id, is_active=True).first_or_404()
    member.delete()
    return {"message": "Member deleted successfully.."}
