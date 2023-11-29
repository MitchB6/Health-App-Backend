from flask_restx import fields

from ..namespace import member_ns

member_model = member_ns.model(
    "Member",
    {
        "member_id": fields.Integer(description="The unique identifier of a member"),
        "username": fields.String(required=True, description="Member's username"),
        "first_name": fields.String(required=True, description="Member's first name"),
        "last_name": fields.String(required=True, description="Member's last name"),
        "email": fields.String(required=True, description="Member's email address"),
        "phone": fields.String(description="Member's phone number"),
        "role_id": fields.Boolean(description="0 for user, 1 for coach, 2 for admin"),
        "city": fields.String(description="Member's city"),
        "state": fields.String(description="Member's state"),
        "zip_code": fields.String(description="Member's zip code"),
        "join_date": fields.DateTime(dt_format='rfc822', description="Date when the member joined"),
        "birthdate": fields.Date(description="Member's birthdate"),
        "height": fields.Integer(description="Member's height in centimeters"),
        "weight": fields.Integer(description="Member's weight in kilograms"),
    }
)
