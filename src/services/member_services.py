from flask_jwt_extended import get_jwt_identity
import re  # regex

from ..models.member_model import Member
from ..models.personalinfo_model import PersonalInfo
from ..extensions import db


def marshal_membersettings(member, personal_info):
    return {
        "member_id": member.member_id,
        "email": member.email,
        "role_id": member.role_id,
        "join_date": member.join_date,
        "first_name": personal_info.first_name,
        "last_name": personal_info.last_name,
        "username": personal_info.username,
        "phone": personal_info.phone,
        "city": personal_info.city,
        "state": personal_info.state,
        "zip_code": personal_info.zip_code,
        "birthdate": personal_info.birthdate,
        "height": personal_info.height,
        "weight": personal_info.weight,
        "age": personal_info.age,
        "gender": personal_info.gender,
    }


def get_member_settings():
    current_member_id = get_jwt_identity()
    member_info = db.session.query(Member, PersonalInfo). \
        filter(Member.member_id == current_member_id). \
        outerjoin(PersonalInfo, Member.member_id ==
                  PersonalInfo.member_id).first()

    member, personal_info = member_info

    if not member:
        return {"message": "Member not found."}, 404

    response = marshal_membersettings(member, personal_info)

    return response, 200


def update_member_settings(data):
    current_member_id = get_jwt_identity()
    member = Member.query.get_or_404(current_member_id)

    allowed_fields_member = ['email']
    allowed_fields_personal_info = ['username', 'phone', 'first_name', 'last_name', 'city', 'state', 'zipcode',
                                    'birthdate', 'height', 'weight', 'age', 'gender']
    for key, value in data.items():
        if key in allowed_fields_member and value is not None:
            setattr(member, key, value)
        elif key in allowed_fields_personal_info and value is not None:
            setattr(member.personal_info, key, value)
    db.session.commit()
    return {"message": "Member settings updated successfully."}, 200


def delete_member():
    current_member_id = get_jwt_identity()
    member = Member.query.filter_by(member_id=current_member_id).first_or_404()
    member.delete()
    return {"message": "Member deleted successfully."}, 200
