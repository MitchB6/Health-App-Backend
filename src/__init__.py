from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .extensions import db,api,migrate
from .models import Member,Password
from .member import member_ns
from .auth import auth_ns
from .home import home_ns

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
    api.add_namespace(home_ns)
    
    # Initialize database
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return app.send_static_file("index.html")
    
    @app.errorhandler(404)
    def not_found(err):
        return app.send_static_file("index.html")
    
    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "Member":Member,
            "Password":Password   
        }
    return app