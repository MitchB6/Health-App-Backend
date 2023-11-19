from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .models import db
from .routes import main
from sqlalchemy.ext.automap import automap_base

# Load env from .env
load_dotenv()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config from
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Extensions
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    db.init_app(app)
    CORS(app)
    
    # Reflect existing tables
    with app.app_context():
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        
    app.register_blueprint(main)
        
    return app
