from flask_restx import fields

from ..extensions import api

signup_model=api.model(
  "SignUp",
  {
    "role_id":fields.Integer(required=True, default=0),
    "username":fields.String(required=True, default="bill"),
    "email":fields.String(required=True, default="bill@email.com"),
    "password":fields.String(required=True, default="12345678"),
    "phone":fields.String(required=False, default="1234567890")
  }
)

login_model=api.model(
  "Login",
  {
    "role_id":fields.Integer(default=0),
    "email":fields.String(default="bill@email.com"),
    "password":fields.String(default="12345678")
  }
)

change_password_model=api.model(
  "ChangePassword",
  {
    "old_password":fields.String(),
    "new_password":fields.String()    
  }
)