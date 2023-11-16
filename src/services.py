from .models import *
from flask_bcrypt import check_password_hash
from . import Base

def authenticate_user(email, password):
    tables = Base.classes
    Member = tables.members
    Password = tables.passwords
    
    member = db.session.query(Member).join(Password, Member.member_id == Password.member_id).filter(Member.email == email).first()
    if member and check_password_hash(member.password.password_hash, password):
        return member
    return None