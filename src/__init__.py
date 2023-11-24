from flask import Flask
from flask_jwt_extended import JWTManager
from config import DevConfig,ProdConfig,TestConfig
from flask_cors import CORS

from .extensions import db,api,migrate
from .models import Member,Password
from .member import member_ns
from .auth import auth_ns

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app,db)
    JWTManager(app)
    api.init_app(app)
    api.add_namespace(member_ns)
    api.add_namespace(auth_ns)
    
    # Initialize database
    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "Member":Member,
            "Password":Password   
        }
    return app