from .extensions import api
from flask_restx import fields

member_model = api.model(
    "Member",
    {
        "member_id": fields.Integer(description="The unique identifier of a member"),
        "first_name": fields.String(required=True, description="Member's first name"),
        "last_name": fields.String(required=True, description="Member's last name"),
        "email": fields.String(required=True, description="Member's email address"),
        "phone": fields.String(description="Member's phone number"),
        "is_coach": fields.Boolean(description="Indicates if the member is a coach"),
        "city": fields.String(description="Member's city"),
        "state": fields.String(description="Member's state"),
        "zip_code": fields.String(description="Member's zip code"),
        "join_date": fields.DateTime(dt_format='rfc822', description="Date when the member joined"),
        "birthdate": fields.Date(description="Member's birthdate"),
        "height": fields.Integer(description="Member's height in centimeters"),
        "weight": fields.Integer(description="Member's weight in kilograms")
    }
)

password_model = api.model(
    "Password",
    {
        "pw_member_id": fields.Integer(description="Member ID associated with the password"),
        "hashed_pw": fields.String(required=True, description="Hashed password"),
        "created_at": fields.DateTime(dt_format='rfc822', description="Creation date of the password"),
        "updated_at": fields.DateTime(dt_format='rfc822', description="Last update date of the password"),
        "password_reset_token": fields.String(description="Password reset token"),
        "password_reset_expiration": fields.DateTime(dt_format='rfc822', description="Expiration date for the password reset token")
    }
)