from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager, create_access_token,
create_refresh_token,jwt_required,get_jwt_identity)
bcrypt=Bcrypt()

def check_password(db_user):
    db_password = db_user.passwords
    if db_user and bcrypt.check_password_hash(db_password.hashed_pw, password):
        #JWT_ACCESS_TOKEN_EXPIRES default(15 minutes)         
        access_token=create_access_token(identity=db_user.member_id)
        refresh_token=create_refresh_token(identity=db_user.member_id)
        
        response_data={
            "access token": access_token,
            "refresh token": refresh_token
        }
        return jsonify(response_data)
    else:
        return jsonify({"message":"Invalid credentials"}), 401