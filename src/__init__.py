from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from .models import *
from .routes import main
from sqlalchemy.ext.automap import automap_base

# Load env from .env
load_dotenv()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config from
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['JWT_SECRET_KET'] = os.getenv('SECRET_KEY')
    
    # Extensions
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)

    init_app(app)
    
    # Reflect existing tables
    with app.app_context():
        Base = automap_base()

        # Double tap to ensure tables modeled == tables of db
        db.create_all()
        
    app.register_blueprint(main)
        
    return app
