from flask_restx import fields

from ..extensions import api

signup_model=api.model(
  "SignUp",
  {
    "role_id":fields.String(required=True,description="Member's role"),
    "username":fields.String(required=True,description="Member's username"),
    "email":fields.String(required=True, description="Member's email address"),
    "password":fields.String(required=True,description="Member's password"),
    "phone":fields.String(required=False,description="Member's phone number"),
  }
)

login_model=api.model(
  "Login",
  {
    "email":fields.String(),
    "password":fields.String()
  }
)

change_password_model=api.model(
  "ChangePassword",
  {
    "old_password":fields.String(),
    "new_password":fields.String()    
  }
)